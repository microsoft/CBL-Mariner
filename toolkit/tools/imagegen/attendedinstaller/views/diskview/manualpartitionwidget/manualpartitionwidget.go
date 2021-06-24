// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package manualpartitionwidget

import (
	"fmt"
	"strings"

	"microsoft.com/pkggen/imagegen/attendedinstaller/primitives/enumfield"
	"microsoft.com/pkggen/imagegen/attendedinstaller/primitives/navigationbar"
	"microsoft.com/pkggen/imagegen/attendedinstaller/uitext"
	"microsoft.com/pkggen/imagegen/attendedinstaller/uiutils"
	"microsoft.com/pkggen/imagegen/configuration"
	"microsoft.com/pkggen/imagegen/diskutils"
	"microsoft.com/pkggen/internal/logger"

	"github.com/gdamore/tcell"
	"github.com/rivo/tview"
)

const (
	confirmButtonIndex      = 1
	addPartitionButtonIndex = 3

	defaultPadding   = 1
	navBarHeight     = 0
	navBarProportion = 1
	noSelection      = -1
	textHeight       = 3
	stripSpaceTags   = false

	// Partition table
	tableHeaderRow         = 0
	tableCellExpansion     = 1
	tableHeaderRowOffset   = tableHeaderRow + 1
	tableHeaderSelectable  = false
	tableRowsSelectable    = true
	tableColumnsSelectable = false

	// Default boot partition
	bootPartitionName   = "boot"
	bootPartitionFormat = "fat32"
	bootPartitionSize   = "9MiB"

	// Page names
	tablePage        = "PARTITIONTABLE"
	addPartitionPage = "ADDPARTITIONFORM"

	maxPartitionSizeRune = '*'

	partitionEntryFormat = "%d%s"
	basePartitionUnit    = diskutils.MiB
	basePartitionLabel   = "MiB"

	maxParittionLabelSize = 32
)

const (
	nameColumn       = iota
	sizeColumn       = iota
	formatColumn     = iota
	mountpointColumn = iota
)

var (
	validPartitionFormats = []string{"ext4", "ext3", "fat32"}
	validSizeUnits        = []string{"MiB", "GiB"}
)

// ManualPartitionWidget contains the disk selection UI
type ManualPartitionWidget struct {
	// Primary elements
	navBar         *navigationbar.NavigationBar
	flex           *tview.Flex
	partitionTable *tview.Table
	spaceLeftText  *tview.TextView
	pages          *tview.Pages

	// Add partition form elements
	addPartitionForm  *tview.Form
	formFlex          *tview.Flex
	formNavBar        *navigationbar.NavigationBar
	formatInput       *enumfield.EnumField
	mountPointInput   *tview.InputField
	nameInput         *tview.InputField
	sizeUnitInput     *enumfield.EnumField
	sizeInput         *tview.InputField
	formSpaceLeftText *tview.TextView

	// Disk state
	bytesRemaining uint64
	deviceIndex    int
	systemDevices  []diskutils.SystemBlockDevice
	bootType       string

	cfg       *configuration.Config
	sysConfig *configuration.SystemConfig

	nextPage     func()
	refreshTitle func()
}

// New creates and returns a new ManualPartitionWidget.
func New(systemDevices []diskutils.SystemBlockDevice, bootType string) *ManualPartitionWidget {
	return &ManualPartitionWidget{
		systemDevices: systemDevices,
		bootType:      bootType,
	}
}

// Initialize initializes the view.
func (mp *ManualPartitionWidget) Initialize(backButtonText string, sysConfig *configuration.SystemConfig, cfg *configuration.Config, app *tview.Application, switchMode, nextPage, previousPage, quit, refreshTitle func()) (err error) {
	if len(mp.systemDevices) == 0 {
		return fmt.Errorf("no devices to install to found")
	}

	mp.sysConfig = sysConfig
	mp.cfg = cfg
	mp.nextPage = nextPage
	mp.refreshTitle = refreshTitle

	mp.navBar = navigationbar.NewNavigationBar().
		AddButton(backButtonText, switchMode).
		AddButton(uitext.DiskButtonRemovePartition, mp.mustRemovePartition).
		AddButton(uitext.DiskButtonAddPartition, mp.addPartition).
		AddButton(uitext.ButtonNext, mp.onNextButton).
		SetAlign(tview.AlignCenter)

	mp.addPartitionForm = tview.NewForm().
		SetButtonsAlign(tview.AlignCenter)

	// Calculate longest label size to align enum input fields
	diskSizeLabelFull := fmt.Sprintf("%s %s", uitext.FormDiskSizeLabel, uitext.FormDiskSizeLabelMaxHelp)
	var maxLabelWidth int
	labels := []string{
		uitext.FormDiskFormatLabel,
		uitext.FormDiskSizeUnitLabel,
		uitext.FormDiskNameLabel,
		uitext.FormDiskMountPointLabel,
		diskSizeLabelFull,
	}
	for _, label := range labels {
		labelLen := len(label)
		if labelLen > maxLabelWidth {
			maxLabelWidth = labelLen
		}
	}

	mp.formatInput = mp.enumInputBox(validPartitionFormats).
		SetLabel(uitext.FormDiskFormatLabel).
		SetLabelWidth(maxLabelWidth).
		SetFieldBackgroundColor(tcell.ColorWhite).
		SetBackgroundColorActivated(tcell.ColorPurple)

	mp.sizeUnitInput = mp.enumInputBox(validSizeUnits).
		SetLabel(uitext.FormDiskSizeUnitLabel).
		SetLabelWidth(maxLabelWidth).
		SetFieldBackgroundColor(tcell.ColorWhite).
		SetBackgroundColorActivated(tcell.ColorPurple)

	mp.nameInput = tview.NewInputField().
		SetLabel(uitext.FormDiskNameLabel).
		SetFieldWidth(maxParittionLabelSize).
		SetAcceptanceFunc(mp.nameInputValidation).
		SetFieldBackgroundColor(tcell.ColorWhite)

	mp.mountPointInput = tview.NewInputField().
		SetLabel(uitext.FormDiskMountPointLabel).
		SetAcceptanceFunc(mp.mountPointInputValidation).
		SetFieldBackgroundColor(tcell.ColorWhite)

	mp.sizeInput = tview.NewInputField().
		SetLabel(diskSizeLabelFull).
		SetAcceptanceFunc(mp.sizeInputValidation).
		SetFieldBackgroundColor(tcell.ColorWhite)

	mp.formSpaceLeftText = tview.NewTextView()

	mp.formNavBar = navigationbar.NewNavigationBar().
		AddButton(uitext.ButtonCancel, func() {
			mp.pages.HidePage(addPartitionPage)
		}).
		AddButton(uitext.ButtonConfirm, mp.onPartitionConfirmButton).
		SetAlign(tview.AlignCenter).
		SetOnFocusFunc(func() {
			mp.formNavBar.SetSelectedButton(confirmButtonIndex)
		}).
		SetOnBlurFunc(func() {
			mp.formNavBar.SetSelectedButton(noSelection)
		})

	mp.addPartitionForm.
		AddFormItem(mp.nameInput).
		AddFormItem(mp.mountPointInput).
		AddFormItem(mp.formatInput).
		AddFormItem(mp.sizeUnitInput).
		AddFormItem(mp.sizeInput).
		AddFormItem(mp.formNavBar).
		SetFieldBackgroundColor(tview.Styles.InverseTextColor)

	mp.partitionTable = tview.NewTable().
		SetSelectable(tableRowsSelectable, tableColumnsSelectable)

	mp.spaceLeftText = tview.NewTextView()

	err = mp.populateTable()
	if err != nil {
		return
	}

	_, formHeight := uiutils.MinFormSize(mp.addPartitionForm)

	formFlex := tview.NewFlex().
		SetDirection(tview.FlexRow).
		AddItem(mp.addPartitionForm, formHeight+mp.formNavBar.GetHeight()+1, 0, true).
		AddItem(mp.formSpaceLeftText, textHeight, 0, true)

	mp.formFlex = uiutils.CenterVerticallyDynamically(formFlex)

	mp.flex = tview.NewFlex().
		SetDirection(tview.FlexRow).
		AddItem(mp.partitionTable, 0, 1, true).
		AddItem(mp.spaceLeftText, textHeight, 0, true).
		AddItem(mp.navBar, navBarHeight, navBarProportion, false)

	mp.pages = tview.NewPages()
	mp.pages.SetChangedFunc(func() {
		app.Draw()
	})

	mp.pages.AddPage(tablePage, mp.flex, true, true)
	mp.pages.AddPage(addPartitionPage, mp.formFlex, true, false)

	// Box styling
	mp.spaceLeftText.SetBorderPadding(defaultPadding, defaultPadding, defaultPadding, defaultPadding)
	mp.partitionTable.SetBorderPadding(defaultPadding, defaultPadding, defaultPadding, defaultPadding)

	mp.formFlex.SetBackgroundColor(tview.Styles.PrimitiveBackgroundColor)
	mp.flex.SetBackgroundColor(tview.Styles.PrimitiveBackgroundColor)

	return
}

// HandleInput handles custom input.
func (mp *ManualPartitionWidget) HandleInput(event *tcell.EventKey) *tcell.EventKey {
	frontPage, _ := mp.pages.GetFrontPage()
	if frontPage == addPartitionPage {
		mp.formSpaceLeftText.SetText(mp.spaceLeftText.GetText(stripSpaceTags))

		switch event.Key() {
		case tcell.KeyUp:
			return tcell.NewEventKey(tcell.KeyBacktab, 0, tcell.ModNone)
		case tcell.KeyDown:
			return tcell.NewEventKey(tcell.KeyTab, 0, tcell.ModNone)
		case tcell.KeyEsc:
			mp.pages.HidePage(addPartitionPage)
		}
	} else {
		// The front page is the partition table
		if mp.navBar.UnfocusedInputHandler(event) {
			return nil
		}

		switch event.Key() {
		case tcell.KeyDelete:
			mp.mustRemovePartition()
		}
	}

	return event
}

// Reset resets the page, undoing any user input.
func (mp *ManualPartitionWidget) Reset() (err error) {
	mp.partitionTable.Clear()
	err = mp.populateTable()
	if err != nil {
		return
	}

	err = mp.updateSpaceLabel()
	if err != nil {
		return
	}

	mp.navBar.ClearUserFeedback()
	mp.navBar.SetSelectedButton(confirmButtonIndex)

	return
}

// Name returns the friendly name of the view.
func (mp *ManualPartitionWidget) Name() string {
	return "MANUALPARTITIONWIDGET"
}

// Title returns the title of the view.
func (mp *ManualPartitionWidget) Title() string {
	if mp.addPartitionForm.HasFocus() {
		return uitext.DiskAddPartitionTitle
	} else {
		return fmt.Sprintf(uitext.DiskAdvanceTitleFmt, mp.systemDevices[mp.deviceIndex].DevicePath)
	}
}

// Primitive returns the primary primitive to be rendered for the view.
func (mp *ManualPartitionWidget) Primitive() tview.Primitive {
	return mp.pages
}

// SetSystemDeviceIndex updates the system device used
func (mp *ManualPartitionWidget) SetSystemDeviceIndex(index int) {
	mp.deviceIndex = index
	mp.flex.SetTitle(fmt.Sprintf(uitext.DiskAdvanceTitleFmt, mp.systemDevices[mp.deviceIndex].DevicePath))
}

func (mp *ManualPartitionWidget) onPartitionConfirmButton() {
	err := mp.validateAddPartitionForm()
	if err != nil {
		mp.formNavBar.SetUserFeedback(err.Error(), tview.Styles.TertiaryTextColor)
	} else {
		var formattedSize string

		sizeText := mp.sizeInput.GetText()
		if sizeText[0] == maxPartitionSizeRune {
			// Expand to all available disk space
			formattedSize = fmt.Sprintf(partitionEntryFormat, mp.bytesRemaining/basePartitionUnit, basePartitionLabel)
		} else {
			currentUnit := mp.sizeUnitInput.GetText()
			formattedSize = fmt.Sprintf("%s%s", sizeText, currentUnit)
		}

		currentFormat := mp.formatInput.GetText()
		mp.addPartitionToTable(mp.nameInput.GetText(), formattedSize, currentFormat, mp.mountPointInput.GetText())
		mp.pages.HidePage(addPartitionPage)
		mp.refreshTitle()
	}
}

func (mp *ManualPartitionWidget) validateAddPartitionForm() (err error) {
	mountPoint := mp.mountPointInput.GetText()
	if mountPoint != "" && mountPoint[0] != '/' {
		return fmt.Errorf(uitext.MountPointStartError)
	}

	if mp.doesMountPointConflict(mountPoint) {
		return fmt.Errorf(uitext.MountPointAlreadyInUseError)
	}

	format := mp.formatInput.GetText()

	currentUnit := mp.sizeUnitInput.GetText()

	sizeText := mp.sizeInput.GetText()
	if sizeText == "" {
		return fmt.Errorf(uitext.NoSizeSpecifiedError)
	}

	if sizeText[0] == '0' {
		return fmt.Errorf(uitext.SizeStartError)
	}

	if sizeText[0] != maxPartitionSizeRune {
		var newPartitionSize uint64
		formattedSize := fmt.Sprintf("%s%s", sizeText, currentUnit)

		newPartitionSize, err = diskutils.SizeAndUnitToBytes(formattedSize)
		if err != nil {
			return
		}

		if newPartitionSize > mp.bytesRemaining {
			return fmt.Errorf(uitext.NotEnoughDiskSpaceError)
		}
	}

	if mountPoint == "/" {
		switch format {
		case "fat32", "swap":
			return fmt.Errorf(uitext.InvalidRootPartitionErrorFormatFmt, format)
		}
	}

	return
}

func (mp *ManualPartitionWidget) resetAddPartitionForm() {
	mp.nameInput.SetText("")
	mp.mountPointInput.SetText("")
	mp.sizeInput.SetText("")
	mp.formSpaceLeftText.SetText(mp.spaceLeftText.GetText(stripSpaceTags))
	mp.formNavBar.ClearUserFeedback()
	mp.formNavBar.SetSelectedButton(noSelection)
	mp.addPartitionForm.SetFocus(0)
	mp.refreshTitle()
}

func (mp *ManualPartitionWidget) populateTable() (err error) {
	headers := []string{
		uitext.DiskNameLabel,
		uitext.DiskSizeLabel,
		uitext.DiskFormatLabel,
		uitext.DiskMountPointLabel,
	}

	for i, header := range headers {
		cell := tview.NewTableCell(header).
			SetTextColor(tview.Styles.SecondaryTextColor).
			SetAlign(tview.AlignCenter).
			SetExpansion(tableCellExpansion).
			SetSelectable(tableHeaderSelectable)

		mp.partitionTable.SetCell(tableHeaderRow, i, cell)
	}

	bootPartitionMountPoint, _, _, err := diskutils.BootPartitionConfig(mp.bootType)
	if err != nil {
		return
	}

	// Add the default boot partition
	err = mp.addPartitionToTable(bootPartitionName, bootPartitionSize, bootPartitionFormat, bootPartitionMountPoint)
	return
}

func (mp *ManualPartitionWidget) bytesRemainingOnDevice() (bytesRemaining uint64, err error) {
	bytesRemaining = mp.systemDevices[mp.deviceIndex].RawDiskSize
	rows := mp.partitionTable.GetRowCount()

	// Leave 1MiB for alignment on both the beginning and end of the disk
	const diskPadding = 2 * basePartitionUnit
	if bytesRemaining <= diskPadding {
		// Prevent underflow on bytesRemaining
		return 0, nil
	}
	bytesRemaining -= diskPadding

	for i := tableHeaderRowOffset; i < rows; i++ {
		partitionSize := mp.partitionTable.GetCell(i, sizeColumn).GetReference().(uint64)
		if bytesRemaining < partitionSize {
			return 0, fmt.Errorf(uitext.PartitionExceedsDiskErrorFmt, i-tableHeaderRowOffset)
		}

		bytesRemaining -= partitionSize
	}

	// Round to the nearest base unit
	bytesRemaining -= bytesRemaining % basePartitionUnit

	return bytesRemaining, nil
}

func (mp *ManualPartitionWidget) updateSpaceLabel() (err error) {
	bytesRemaining, err := mp.bytesRemainingOnDevice()
	if err != nil {
		return
	}

	mp.spaceLeftText.SetText(fmt.Sprintf(uitext.DiskSpaceLeftFmt, diskutils.BytesToSizeAndUnit(bytesRemaining)))
	mp.bytesRemaining = bytesRemaining

	return
}

func (mp *ManualPartitionWidget) addPartitionToTable(name, size, format, mountPoint string) (err error) {
	newCells := []string{name, size, format, mountPoint}
	row := mp.partitionTable.GetRowCount()

	for i, cellText := range newCells {
		cell := tview.NewTableCell(cellText).
			SetAlign(tview.AlignCenter)

		mp.partitionTable.SetCell(row, i, cell)
	}

	sizeInBytes, err := diskutils.SizeAndUnitToBytes(size)
	if err != nil {
		return
	}

	mp.partitionTable.GetCell(row, sizeColumn).SetReference(sizeInBytes)
	err = mp.updateSpaceLabel()
	return
}

func (mp *ManualPartitionWidget) addPartition() {
	if mp.bytesRemaining == 0 {
		mp.navBar.SetUserFeedback(uitext.NotEnoughDiskSpaceError, tview.Styles.TertiaryTextColor)
		return
	}

	mp.navBar.ClearUserFeedback()
	mp.resetAddPartitionForm()
	mp.pages.ShowPage(addPartitionPage)
	mp.refreshTitle()
}

// mustRemovePartition will panic if the space label cannot be updated
func (mp *ManualPartitionWidget) mustRemovePartition() {
	mp.navBar.ClearUserFeedback()

	row, _ := mp.partitionTable.GetSelection()

	if row == tableHeaderRow {
		mp.navBar.SetUserFeedback(uitext.NoPartitionSelectedError, tview.Styles.TertiaryTextColor)
		return
	}

	mp.partitionTable.RemoveRow(row)

	// On error there is no clean way to bubble up the error as this routine is invoked from UI threads,
	// so panic as this is unexpected.
	err := mp.updateSpaceLabel()
	logger.PanicOnError(err, "Failed to update space label")

	return
}

func (mp *ManualPartitionWidget) unmarshalPartitionTable() (err error) {
	const (
		targetDiskType     = "path"
		partitionTableType = "gpt"

		rootMountPoint     = "/"
		bootPartitionIndex = 0
	)

	_, bootMountOptions, bootFlags, err := diskutils.BootPartitionConfig(mp.bootType)
	if err != nil {
		return
	}

	rows := mp.partitionTable.GetRowCount() - tableHeaderRowOffset // Skip header
	if rows == 0 {
		return fmt.Errorf(uitext.NoPartitionsError)
	}

	partitions := make([]configuration.Partition, rows)
	partitionSettings := make([]configuration.PartitionSetting, rows)

	// Start the first partition (boot) at the start of the disk (1MiB)
	var diskCursor uint64
	diskCursor = basePartitionUnit

	foundRootPartition := false

	// First partition - must be boot
	if mp.partitionTable.GetCell(bootPartitionIndex+tableHeaderRowOffset, formatColumn).Text != bootPartitionFormat {
		return fmt.Errorf(uitext.InvalidBootPartitionErrorFmt, bootPartitionFormat)
	}

	// Update boot partition
	partitions[bootPartitionIndex].Flags = bootFlags
	partitionSettings[bootPartitionIndex].MountOptions = bootMountOptions

	for i := range partitions {
		currentRow := i + tableHeaderRowOffset

		partitionSize := mp.partitionTable.GetCell(currentRow, sizeColumn).GetReference().(uint64)
		if partitionSize%basePartitionUnit != 0 {
			partitionFriendlySize := mp.partitionTable.GetCell(currentRow, sizeColumn).Text
			return fmt.Errorf(uitext.UnexpectedPartitionErrorFmt, partitionFriendlySize)
		}

		partitions[i].ID = mp.partitionTable.GetCell(currentRow, nameColumn).Text
		partitionSettings[i].ID = partitions[i].ID
		partitions[i].Name = partitions[i].ID

		partitions[i].FsType = mp.partitionTable.GetCell(currentRow, formatColumn).Text
		partitionSettings[i].MountPoint = mp.partitionTable.GetCell(currentRow, mountpointColumn).Text

		nextCursor := diskCursor + partitionSize
		partitions[i].Start = diskCursor / basePartitionUnit
		partitions[i].End = nextCursor / basePartitionUnit

		if partitionSettings[i].MountPoint == rootMountPoint {
			foundRootPartition = true
		}

		diskCursor = nextCursor
	}

	if !foundRootPartition {
		return fmt.Errorf(uitext.InvalidRootPartitionErrorFmt, rootMountPoint)
	}

	disk := configuration.Disk{}
	disk.PartitionTableType = partitionTableType
	disk.TargetDisk = configuration.TargetDisk{
		Type:  targetDiskType,
		Value: mp.systemDevices[mp.deviceIndex].DevicePath,
	}
	disk.Partitions = partitions

	mp.sysConfig.BootType = mp.bootType
	mp.sysConfig.PartitionSettings = partitionSettings
	mp.cfg.Disks = []configuration.Disk{disk}

	// Flag the root for use with device mapper
	if mp.sysConfig.ReadOnlyVerityRoot.Enable {
		rootDiskPart := mp.cfg.GetDiskPartByID(mp.sysConfig.GetRootPartitionSetting().ID)
		if rootDiskPart == nil {
			return fmt.Errorf(uitext.InvalidRootDeviceMapperError)
		}
		rootDiskPart.Flags = append(rootDiskPart.Flags, configuration.PartitionFlagDeviceMapperRoot)
	}

	return
}

func (mp *ManualPartitionWidget) doesMountPointConflict(mountPoint string) bool {
	if mountPoint == "" {
		return false
	}

	rows := mp.partitionTable.GetRowCount()

	for i := tableHeaderRowOffset; i < rows; i++ {
		currentMountPoint := mp.partitionTable.GetCell(i, mountpointColumn).Text
		if currentMountPoint == mountPoint {
			return true
		}
	}

	return false
}

func (mp *ManualPartitionWidget) sizeInputValidation(textToCheck string, lastChar rune) bool {
	// Support * (maxPartitionSizeRune) iff its the first and only character
	if len(textToCheck) == 1 && lastChar == maxPartitionSizeRune {
		return true
	}

	if textToCheck[0] == '0' {
		mp.formNavBar.SetUserFeedback(uitext.SizeStartError, tview.Styles.TertiaryTextColor)
		return false
	}

	if lastChar < '0' || lastChar > '9' {
		mp.formNavBar.SetUserFeedback(uitext.SizeInvalidCharacterError, tview.Styles.TertiaryTextColor)
		return false
	}

	return true
}

func (mp *ManualPartitionWidget) mountPointInputValidation(textToCheck string, lastChar rune) bool {
	if textToCheck[0] != '/' {
		mp.formNavBar.SetUserFeedback(uitext.MountPointStartError, tview.Styles.TertiaryTextColor)
		return false
	}

	if lastChar != '/' && !strings.ContainsRune(uitext.AlphaNumeric, lastChar) {
		mp.formNavBar.SetUserFeedback(uitext.MountPointInvalidCharacterError, tview.Styles.TertiaryTextColor)
		return false
	}

	return true
}

func (mp *ManualPartitionWidget) nameInputValidation(textToCheck string, lastChar rune) bool {
	if len(textToCheck) > maxParittionLabelSize {
		return false
	}

	if !strings.ContainsRune(uitext.AlphaNumeric, lastChar) {
		mp.formNavBar.SetUserFeedback(uitext.NameInvalidCharacterError, tview.Styles.TertiaryTextColor)
		return false
	}

	return true
}

func (mp *ManualPartitionWidget) onNextButton() {
	mp.navBar.ClearUserFeedback()
	err := mp.unmarshalPartitionTable()
	if err != nil {
		mp.navBar.SetUserFeedback(err.Error(), tview.Styles.TertiaryTextColor)
	} else {
		mp.nextPage()
	}
}

// enumInputBox returns an input box that only allows values
// from elements to appear and produces helpful error message for
// every unhandled input
func (mp *ManualPartitionWidget) enumInputBox(elements []string) *enumfield.EnumField {
	field := enumfield.NewEnumField(elements)
	// Add helpful message when user presses any key we do not process
	field.SetInputCapture(func(event *tcell.EventKey) *tcell.EventKey {
		key := event.Key()
		switch key {
		case tcell.KeyEnter, tcell.KeyEscape,
			tcell.KeyDown, tcell.KeyTab,
			tcell.KeyUp, tcell.KeyBacktab,
			tcell.KeyLeft, tcell.KeyRight:
			// Navigation keys - pass
			return event
		default:
			mp.formNavBar.SetUserFeedback(uitext.EnumNavigationFeedback, tview.Styles.TertiaryTextColor)
			return nil
		}
	})
	return field
}
