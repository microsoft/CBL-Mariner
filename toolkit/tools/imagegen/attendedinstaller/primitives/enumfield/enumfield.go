// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package enumfield

import (
	"math"

	"github.com/gdamore/tcell"
	"github.com/rivo/tview"
)

type EnumField struct {
	*tview.Box

	// The label of the field
	label string

	// Maximum width of the label, or 0 for label's length
	labelWidth int

	// Options to choose from
	options []string

	// Index of the currently selected option
	selectedOption int

	// The label color.
	labelColor tcell.Color

	// The label color when this item is selected.
	labelColorActivated tcell.Color

	// The text color.
	textColor tcell.Color

	// The text color when this item is selected.
	textColorActivated tcell.Color

	// The background color.
	backgroundColor tcell.Color

	// The background color when this item is selected.
	backgroundColorActivated tcell.Color

	// A callback invoked when the user leaves this form item
	onFinished func(tcell.Key)

	// A callback invoked when this primitive receives focus.
	onFocus func()

	// A callback invoked when this primitive loses focus.
	onBlur func()
}

// NewEnumField returns a new navigation bar.
func NewEnumField(options []string) *EnumField {
	return &EnumField{
		Box:                      tview.NewBox(),
		backgroundColor:          tview.Styles.PrimitiveBackgroundColor,
		backgroundColorActivated: tview.Styles.ContrastBackgroundColor,
		labelColor:               tview.Styles.SecondaryTextColor,
		labelColorActivated:      tview.Styles.ContrastSecondaryTextColor,
		textColor:                tview.Styles.PrimaryTextColor,
		textColorActivated:       tview.Styles.PrimaryTextColor,
		options:                  options,
	}
}

// SetLabelColor sets the color of button text.
func (n *EnumField) SetLabelColor(color tcell.Color) *EnumField {
	n.labelColor = color
	return n
}

// SetLabelColorActivated sets the color of button text when the button is
// selected.
func (n *EnumField) SetLabelColorActivated(color tcell.Color) *EnumField {
	n.labelColorActivated = color
	return n
}

// SetNavBackgroundColor sets the background color.
func (n *EnumField) SetFieldBackgroundColor(color tcell.Color) *EnumField {
	n.backgroundColor = color
	return n
}

// SetBackgroundColorActivated sets the background color of the button text when
// the button is selected.
func (n *EnumField) SetBackgroundColorActivated(color tcell.Color) *EnumField {
	n.backgroundColorActivated = color
	return n
}

// Draw renders this primitive onto the screen.
func (n *EnumField) Draw(screen tcell.Screen) {

	// Update dimensions
	n.Box.Draw(screen)

	// Obtain dimensions
	x, y, width, height := n.GetInnerRect()
	rightLimit := x + width
	if height < 1 || rightLimit <= x {
		return
	}

	// Draw label.
	// Make sure labelWidth is not greater than n.labelWidth
	labelWidth := rightLimit - x
	if (n.labelWidth > 0) && (n.labelWidth < labelWidth) {
		labelWidth = n.labelWidth
	}
	tview.Print(screen, n.label, x, y, labelWidth, tview.AlignLeft, n.labelColor)
	// Always move to the edge to align input fields
	x += n.labelWidth

	// Don't draw the option part if there are no options
	if len(n.options) == 0 {
		return
	}

	// get as much space as needed or available
	fieldWidth := math.MaxInt32
	if rightLimit-x < fieldWidth {
		fieldWidth = rightLimit - x
	}

	// Draw the background
	var (
		fieldStyle tcell.Style
		textColor  tcell.Color
	)

	if n.HasFocus() {
		fieldStyle = tcell.StyleDefault.Background(n.backgroundColorActivated)
		textColor = n.textColorActivated
	} else {
		fieldStyle = tcell.StyleDefault.Background(n.backgroundColor)
		textColor = n.textColor
	}

	for index := 0; index < len(n.options[n.selectedOption]); index++ {
		screen.SetContent(x+index, y, ' ', nil, fieldStyle)
	}

	// Draw the text
	text := n.options[n.selectedOption]
	tview.Print(screen, tview.Escape(text), x, y, fieldWidth, tview.AlignLeft, textColor)
}

// InputHandler returns the handler for this primitive.
func (n *EnumField) InputHandler() func(event *tcell.EventKey, setFocus func(p tview.Primitive)) {
	return n.WrapInputHandler(func(event *tcell.EventKey, setFocus func(p tview.Primitive)) {
		key := event.Key()
		switch key {
		case tcell.KeyLeft:
			n.selectedOption--
			if n.selectedOption < 0 {
				n.selectedOption = len(n.options) - 1
			}
		case tcell.KeyRight:
			n.selectedOption++
			if n.selectedOption == len(n.options) {
				n.selectedOption = 0
			}
		case tcell.KeyDown, tcell.KeyUp, tcell.KeyEnter,
			tcell.KeyEscape, tcell.KeyTab, tcell.KeyBacktab:
			n.onFinished(key)
		}
	})
}

// GetLabel returns the text to be displayed before the input area.
func (n *EnumField) GetLabel() string {
	return n.label
}

// GetFieldWidth obtains a screen width of the input area. A value of 0 means
// extend as much as possible.
func (n *EnumField) GetFieldWidth() int {
	// Same as the text length
	return 0
}

// SetFormAttributes sets attributes shared by all form items. Only bgColor is considered for bg colors.
func (n *EnumField) SetFormAttributes(labelWidth int, labelColor, bgColor, fieldTextColor, fieldBgColor tcell.Color) tview.FormItem {
	n.labelWidth = labelWidth
	n.labelColor = labelColor
	n.textColor = fieldTextColor
	n.backgroundColor = bgColor

	return n
}

// SetFinishedFunc sets a callback invoked when the user leaves this form item.
func (n *EnumField) SetFinishedFunc(handler func(key tcell.Key)) tview.FormItem {
	n.onFinished = handler
	return n
}

// SetOnFocusFunc sets a callback invoked when this primitive receives focus.
func (n *EnumField) SetOnFocusFunc(handler func()) *EnumField {
	n.onFocus = handler
	return n
}

// SetOnBlurFunc sets a callback invoked when this primitive loses focus.
func (n *EnumField) SetOnBlurFunc(handler func()) *EnumField {
	n.onBlur = handler
	return n
}

// Focus is called when this primitive receives focus.
func (n *EnumField) Focus(delegate func(p tview.Primitive)) {
	if n.onFocus != nil {
		n.onFocus()
	}

	n.Box.Focus(delegate)
}

// Blur is called when this primitive loses focus.
func (n *EnumField) Blur() {
	if n.onBlur != nil {
		n.onBlur()
	}
	n.Box.Blur()
}

// GetText returns currently selected text
func (n *EnumField) GetText() string {
	return n.options[n.selectedOption]
}

// SetLabel sets label and returns the updated object.
func (n *EnumField) SetLabel(x string) *EnumField {
	n.label = x
	n.Box.SetTitle(n.label)
	return n
}

// SetLabelWidth sets the screen width of the label. A value of 0 will cause the
// primitive to use the width of the label string.
func (n *EnumField) SetLabelWidth(width int) *EnumField {
	n.labelWidth = width
	return n
}

// GetLabelWidth returns width of the label field.
func (n *EnumField) GetLabelWidth() int {
	return n.labelWidth
}
