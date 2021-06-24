// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkgjson

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"microsoft.com/pkggen/internal/versioncompare"
)

func TestBasicInterval(t *testing.T) {
	p1 := &PackageVer{Version: "1"}
	interval, err := p1.Interval()
	assert.NoError(t, err)
	assert.True(t, interval.LowerBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.UpperBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.LowerInclusive)
	assert.True(t, interval.UpperInclusive)

	p1 = &PackageVer{Version: "1", Condition: "="}
	interval, err = p1.Interval()
	assert.NoError(t, err)
	assert.True(t, interval.LowerBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.UpperBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.LowerInclusive)
	assert.True(t, interval.UpperInclusive)
}

func TestIntervalPrint(t *testing.T) {
	p1 := PackageVer{Version: "1"}
	i1, _ := p1.Interval()
	p2 := PackageVer{Version: "1", Condition: ">"}
	i2, _ := p2.Interval()
	p3 := PackageVer{Version: "1", Condition: ">="}
	i3, _ := p3.Interval()
	p4 := PackageVer{Version: "1", Condition: ">", SVersion: "2", SCondition: "<"}
	i4, _ := p4.Interval()
	assert.Equal(t, "[1,1]", i1.String())
	assert.Equal(t, "(1,MAX_VER]", i2.String())
	assert.Equal(t, "[1,MAX_VER]", i3.String())
	assert.Equal(t, "(1,2)", i4.String())

}

func TestBasicIntervalSVersion(t *testing.T) {
	p1 := &PackageVer{SVersion: "1"}
	interval, err := p1.Interval()
	assert.NoError(t, err)
	assert.True(t, interval.LowerBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.UpperBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.LowerInclusive)
	assert.True(t, interval.UpperInclusive)

	p1 = &PackageVer{SVersion: "1", SCondition: "="}
	interval, err = p1.Interval()
	assert.NoError(t, err)
	assert.True(t, interval.LowerBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.UpperBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.LowerInclusive)
	assert.True(t, interval.UpperInclusive)
}

func TestNoDataInterval(t *testing.T) {
	p1 := &PackageVer{}
	interval, err := p1.Interval()
	assert.NoError(t, err)
	assert.True(t, interval.UpperBound.Compare(versioncompare.NewMax()) == 0)
	assert.True(t, interval.LowerBound.Compare(versioncompare.NewMin()) == 0)
	assert.True(t, interval.LowerInclusive)
	assert.True(t, interval.UpperInclusive)
}

func TestSingleConditionalIntervalGreater(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: ">"}
	interval, err := p1.Interval()
	assert.NoError(t, err)
	assert.True(t, interval.LowerBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.UpperBound.Compare(versioncompare.NewMax()) == 0)
	assert.False(t, interval.LowerInclusive)
	assert.True(t, interval.UpperInclusive)
}

func TestSingleConditionalIntervalGreaterOrEqual(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: ">="}
	interval, err := p1.Interval()
	assert.NoError(t, err)
	assert.True(t, interval.LowerBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.UpperBound.Compare(versioncompare.NewMax()) == 0)
	assert.True(t, interval.LowerInclusive)
	assert.True(t, interval.UpperInclusive)
}

func TestSingleConditionalIntervalLess(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: "<"}
	interval, err := p1.Interval()
	assert.NoError(t, err)
	assert.True(t, interval.UpperBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.LowerBound.Compare(versioncompare.NewMin()) == 0)
	assert.False(t, interval.UpperInclusive)
	assert.True(t, interval.LowerInclusive)
}

func TestSingleConditionalIntervalLessOrEqual(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: "<="}
	interval, err := p1.Interval()
	assert.NoError(t, err)
	assert.True(t, interval.UpperBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.LowerBound.Compare(versioncompare.NewMin()) == 0)
	assert.True(t, interval.UpperInclusive)
	assert.True(t, interval.LowerInclusive)
}

func TestCreateRangeBothInclusive(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: ">=", SVersion: "2", SCondition: "<="}
	interval, err := p1.Interval()
	assert.NoError(t, err)
	assert.True(t, interval.LowerBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.UpperBound.Compare(versioncompare.New("2")) == 0)
	assert.True(t, interval.UpperInclusive)
	assert.True(t, interval.LowerInclusive)
}

func TestCreateRangeInverted(t *testing.T) {
	p1 := &PackageVer{Version: "2", Condition: "<=", SVersion: "1", SCondition: ">="}
	interval, err := p1.Interval()
	assert.NoError(t, err)
	assert.True(t, interval.LowerBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.UpperBound.Compare(versioncompare.New("2")) == 0)
	assert.True(t, interval.UpperInclusive)
	assert.True(t, interval.LowerInclusive)
}

func TestCreateRangeOneInclusive(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: ">", SVersion: "2", SCondition: "<="}
	interval, err := p1.Interval()
	assert.NoError(t, err)
	assert.True(t, interval.LowerBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.UpperBound.Compare(versioncompare.New("2")) == 0)
	assert.True(t, interval.UpperInclusive)
	assert.False(t, interval.LowerInclusive)

	p1 = &PackageVer{Version: "1", Condition: ">=", SVersion: "2", SCondition: "<"}
	interval, err = p1.Interval()
	assert.NoError(t, err)
	assert.True(t, interval.LowerBound.Compare(versioncompare.New("1")) == 0)
	assert.True(t, interval.UpperBound.Compare(versioncompare.New("2")) == 0)
	assert.False(t, interval.UpperInclusive)
	assert.True(t, interval.LowerInclusive)
}

func TestMembershipEquality(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: "="}
	p2 := &PackageVer{Version: "1", Condition: "="}
	interval1, err := p1.Interval()
	assert.NoError(t, err)
	interval2, err := p2.Interval()
	assert.NoError(t, err)
	assert.True(t, interval1.Satisfies(&interval2))
}

func TestMembershipInequality(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: "="}
	p2 := &PackageVer{Version: "2", Condition: "="}
	interval1, err := p1.Interval()
	assert.NoError(t, err)
	interval2, err := p2.Interval()
	assert.NoError(t, err)
	assert.False(t, interval1.Satisfies(&interval2))
}

func TestMembershipInInterval(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: ">", SVersion: "3", SCondition: "<"}
	p2 := &PackageVer{Version: "2", Condition: "="}
	interval1, err := p1.Interval()
	assert.NoError(t, err)
	interval2, err := p2.Interval()
	assert.NoError(t, err)

	assert.True(t, interval1.Satisfies(&interval2))
}

func TestMembershipOutsideInterval(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: ">", SVersion: "3", SCondition: "<"}
	p2 := &PackageVer{Version: "4", Condition: "="}
	interval1, err := p1.Interval()
	assert.NoError(t, err)
	interval2, err := p2.Interval()
	assert.NoError(t, err)

	assert.False(t, interval1.Satisfies(&interval2))
}

func TestMembershipEdgeInvalidInterval(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: ">", SVersion: "3", SCondition: "<"}
	tests := []*PackageVer{
		&PackageVer{Version: "1", Condition: "="},
		&PackageVer{Version: "1", Condition: "<"},
		&PackageVer{Version: "1", Condition: "<="},
		&PackageVer{Version: "3", Condition: "="},
		&PackageVer{Version: "3", Condition: ">"},
		&PackageVer{Version: "3", Condition: ">="},
	}
	interval1, err := p1.Interval()
	assert.NoError(t, err)
	for _, pkg := range tests {
		interval2, err := pkg.Interval()
		assert.NoError(t, err)
		assert.False(t, interval1.Satisfies(&interval2))
	}
}

func TestMembershipEdgeValidInterval(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: ">=", SVersion: "3", SCondition: "<="}
	tests := []*PackageVer{
		&PackageVer{Version: "1", Condition: "="},
		&PackageVer{Version: "1", Condition: "<="},
		&PackageVer{Version: "3", Condition: "="},
		&PackageVer{Version: "3", Condition: ">="},
	}
	interval1, err := p1.Interval()
	assert.NoError(t, err)
	for _, pkg := range tests {
		interval2, err := pkg.Interval()
		assert.NoError(t, err)
		assert.True(t, interval1.Satisfies(&interval2))
	}
}

func TestSubsetValidInside(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: ">=", SVersion: "3", SCondition: "<="}
	p2 := &PackageVer{Version: "1", Condition: ">"}
	p3 := &PackageVer{Version: "3", Condition: "<"}
	interval1, err := p1.Interval()
	assert.NoError(t, err)
	interval2, err := p2.Interval()
	assert.NoError(t, err)
	interval3, err := p3.Interval()
	assert.NoError(t, err)

	assert.True(t, interval1.Satisfies(&interval2))
	assert.True(t, interval1.Satisfies(&interval3))
	assert.False(t, interval1.Contains(&interval2))
	assert.False(t, interval1.Contains(&interval3))
}

func TestSubsetValidOutside(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: ">=", SVersion: "3", SCondition: "<="}
	p2 := &PackageVer{Version: "0", Condition: ">"}
	p3 := &PackageVer{Version: "4", Condition: "<"}
	interval1, err := p1.Interval()
	assert.NoError(t, err)
	interval2, err := p2.Interval()
	assert.NoError(t, err)
	interval3, err := p3.Interval()
	assert.NoError(t, err)

	assert.True(t, interval1.Satisfies(&interval2))
	assert.True(t, interval1.Satisfies(&interval3))
	assert.False(t, interval1.Contains(&interval2))
	assert.False(t, interval1.Contains(&interval3))
}

func TestSubsetInvalid(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: ">=", SVersion: "3", SCondition: "<="}
	p2 := &PackageVer{Version: "1", Condition: ">"}
	p3 := &PackageVer{Version: "1", Condition: ">"}
	interval1, err := p1.Interval()
	assert.NoError(t, err)
	interval2, err := p2.Interval()
	assert.NoError(t, err)
	interval3, err := p3.Interval()
	assert.NoError(t, err)

	assert.True(t, interval1.Satisfies(&interval2))
	assert.True(t, interval1.Satisfies(&interval3))
	assert.False(t, interval1.Contains(&interval2))
	assert.False(t, interval1.Contains(&interval3))
}

func TestInvalidRange(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: "<=", SVersion: "2", SCondition: "<="}
	p2 := &PackageVer{Version: "1", Condition: ">=", SVersion: "2", SCondition: ">="}
	p3 := &PackageVer{Version: "1", Condition: "=", SVersion: "2", SCondition: ">="}
	p4 := &PackageVer{Version: "1", Condition: "=", SVersion: "2", SCondition: "<="}
	_, err := p1.Interval()
	assert.Error(t, err)
	_, err = p2.Interval()
	assert.Error(t, err)
	_, err = p3.Interval()
	assert.Error(t, err)
	_, err = p4.Interval()
	assert.Error(t, err)
}

func TestIntervalEquality(t *testing.T) {
	p1 := &PackageVer{Version: "1", Condition: ">=", SVersion: "2", SCondition: "<="}
	p2 := &PackageVer{Version: "2", Condition: "<=", SVersion: "1", SCondition: ">="}
	p3 := &PackageVer{Version: "2", Condition: "<", SVersion: "1", SCondition: ">="}
	interval1, err := p1.Interval()
	assert.NoError(t, err)
	interval2, err := p2.Interval()
	assert.NoError(t, err)
	interval3, err := p3.Interval()
	assert.NoError(t, err)

	assert.True(t, interval1.Equal(&interval2))
	assert.False(t, interval1.Equal(&interval3))
}

func TestIntervalCompare(t *testing.T) {
	low := &PackageVer{Version: "1"}
	high := &PackageVer{Version: "2"}
	intervalLow, err := low.Interval()
	assert.NoError(t, err)
	intervalHigh, err := high.Interval()
	assert.NoError(t, err)
	assert.Equal(t, -1, intervalLow.Compare(&intervalHigh))
	assert.Equal(t, 1, intervalHigh.Compare(&intervalLow))
	assert.Equal(t, 0, intervalLow.Compare(&intervalLow))
}

func TestIntervalCompareWithLowerInclusion(t *testing.T) {
	low := &PackageVer{Version: "1", Condition: "<"}
	high := &PackageVer{Version: "1", Condition: "<="}
	intervalLow, err := low.Interval()
	assert.NoError(t, err)
	intervalHigh, err := high.Interval()
	assert.NoError(t, err)
	assert.Equal(t, -1, intervalLow.Compare(&intervalHigh))
	assert.Equal(t, 1, intervalHigh.Compare(&intervalLow))
	assert.Equal(t, 0, intervalLow.Compare(&intervalLow))
}

func TestIntervalCompareWithHigherInclusion(t *testing.T) {
	low := &PackageVer{Version: "1", Condition: ">", SVersion: "2", SCondition: "<"}
	high := &PackageVer{Version: "1", Condition: ">", SVersion: "2", SCondition: "<="}
	intervalLow, err := low.Interval()
	assert.NoError(t, err)
	intervalHigh, err := high.Interval()
	assert.NoError(t, err)
	assert.Equal(t, -1, intervalLow.Compare(&intervalHigh))
	assert.Equal(t, 1, intervalHigh.Compare(&intervalLow))
	assert.Equal(t, 0, intervalLow.Compare(&intervalLow))
}

func TestIntervalCompareWithLowerExclusion(t *testing.T) {
	low := &PackageVer{Version: "1", Condition: ">="}
	high := &PackageVer{Version: "1", Condition: ">"}
	intervalLow, err := low.Interval()
	assert.NoError(t, err)
	intervalHigh, err := high.Interval()
	assert.NoError(t, err)
	assert.Equal(t, -1, intervalLow.Compare(&intervalHigh))
	assert.Equal(t, 1, intervalHigh.Compare(&intervalLow))
	assert.Equal(t, 0, intervalLow.Compare(&intervalLow))
}

func TestIntervalCompareWithHigherExclusion(t *testing.T) {
	low := &PackageVer{Version: "1", Condition: ">=", SVersion: "2", SCondition: "<"}
	high := &PackageVer{Version: "1", Condition: ">", SVersion: "2", SCondition: "<"}
	intervalLow, err := low.Interval()
	assert.NoError(t, err)
	intervalHigh, err := high.Interval()
	assert.NoError(t, err)
	assert.Equal(t, -1, intervalLow.Compare(&intervalHigh))
	assert.Equal(t, 1, intervalHigh.Compare(&intervalLow))
}

func TestShouldCorrectlyConvertPackageNameWithoutVersionConstraints(t *testing.T) {
	packageVer, err := PackagesListEntryToPackageVer("gcc-devel")

	assert.NoError(t, err)
	assert.Equal(t, "gcc-devel", packageVer.Name)
	assert.Equal(t, "", packageVer.Condition)
	assert.Equal(t, "", packageVer.SCondition)
	assert.Equal(t, "", packageVer.SVersion)
	assert.Equal(t, "", packageVer.Version)
}

func TestShouldCorrectlyConvertPackageNameWithEqualsVersionConstraint(t *testing.T) {
	packageVer, err := PackagesListEntryToPackageVer("gcc-devel=9.1.0")

	assert.NoError(t, err)
	assert.Equal(t, "gcc-devel", packageVer.Name)
	assert.Equal(t, "=", packageVer.Condition)
	assert.Equal(t, "", packageVer.SCondition)
	assert.Equal(t, "", packageVer.SVersion)
	assert.Equal(t, "9.1.0", packageVer.Version)
}

func TestShouldCorrectlyConvertPackageNameWithGreaterEqualsVersionConstraint(t *testing.T) {
	packageVer, err := PackagesListEntryToPackageVer("gcc-devel>=9.1.0")

	assert.NoError(t, err)
	assert.Equal(t, "gcc-devel", packageVer.Name)
	assert.Equal(t, ">=", packageVer.Condition)
	assert.Equal(t, "", packageVer.SCondition)
	assert.Equal(t, "", packageVer.SVersion)
	assert.Equal(t, "9.1.0", packageVer.Version)
}

func TestShouldCorrectlyConvertPackageNameWithGreaterVersionConstraint(t *testing.T) {
	packageVer, err := PackagesListEntryToPackageVer("gcc-devel>9.1.0")

	assert.NoError(t, err)
	assert.Equal(t, "gcc-devel", packageVer.Name)
	assert.Equal(t, ">", packageVer.Condition)
	assert.Equal(t, "", packageVer.SCondition)
	assert.Equal(t, "", packageVer.SVersion)
	assert.Equal(t, "9.1.0", packageVer.Version)
}

func TestShouldCorrectlyConvertPackageNameWithLesserEqualsVersionConstraint(t *testing.T) {
	packageVer, err := PackagesListEntryToPackageVer("gcc-devel<=9.1.0")

	assert.NoError(t, err)
	assert.Equal(t, "gcc-devel", packageVer.Name)
	assert.Equal(t, "<=", packageVer.Condition)
	assert.Equal(t, "", packageVer.SCondition)
	assert.Equal(t, "", packageVer.SVersion)
	assert.Equal(t, "9.1.0", packageVer.Version)
}

func TestShouldCorrectlyConvertPackageNameWithLesserVersionConstraint(t *testing.T) {
	packageVer, err := PackagesListEntryToPackageVer("gcc-devel<9.1.0")

	assert.NoError(t, err)
	assert.Equal(t, "gcc-devel", packageVer.Name)
	assert.Equal(t, "<", packageVer.Condition)
	assert.Equal(t, "", packageVer.SCondition)
	assert.Equal(t, "", packageVer.SVersion)
	assert.Equal(t, "9.1.0", packageVer.Version)
}

func TestShouldCorrectlyConvertPackageNameWithAllowedWhitespaces(t *testing.T) {
	packageVer, err := PackagesListEntryToPackageVer("  gcc-devel\t\t< 9.1.0    ")

	assert.NoError(t, err)
	assert.Equal(t, "gcc-devel", packageVer.Name)
	assert.Equal(t, "<", packageVer.Condition)
	assert.Equal(t, "", packageVer.SCondition)
	assert.Equal(t, "", packageVer.SVersion)
	assert.Equal(t, "9.1.0", packageVer.Version)
}

func TestShouldFailToConvertPackageListEntryStartingWithInvalidCharacter(t *testing.T) {
	_, err := PackagesListEntryToPackageVer("=gcc-devel")

	assert.Error(t, err)
}

func TestShouldFailToConvertPackageListEntryWithIncompleteComparison(t *testing.T) {
	_, err := PackagesListEntryToPackageVer("gcc-devel=")

	assert.Error(t, err)
}

func TestShouldFailToConvertPackageListEntryWithInvalidComparison(t *testing.T) {
	_, err := PackagesListEntryToPackageVer("gcc-devel=>9.1.0")

	assert.Error(t, err)
}

func TestShouldFailToConvertPackageListEntryWithWhitespacesInComparison(t *testing.T) {
	_, err := PackagesListEntryToPackageVer("gcc-devel< =9.1.0")

	assert.Error(t, err)
}

func TestShouldFailToConvertPackageListEntryWithWhitespacesInName(t *testing.T) {
	_, err := PackagesListEntryToPackageVer("gcc devel")

	assert.Error(t, err)
}

func TestShouldFailToConvertPackageListEntryWithWhitespacesInVersion(t *testing.T) {
	_, err := PackagesListEntryToPackageVer("gcc-devel<9 1.0")

	assert.Error(t, err)
}
