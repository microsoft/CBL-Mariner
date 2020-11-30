// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's Users configuration schema.

package configuration

import (
	"fmt"
	"strconv"
)

type User struct {
	Name                string   `json:"Name"`
	UID                 string   `json:"UID"`
	PasswordHashed      bool     `json:"PasswordHashed"`
	Password            string   `json:"Password"`
	PasswordExpiresDays int64    `json:"PasswordExpiresDays"`
	SSHPubKeyPaths      []string `json:"SSHPubKeyPaths"`
	PrimaryGroup        string   `json:"PrimaryGroup"`
	SecondaryGroups     []string `json:"SecondaryGroups"`
	StartupCommand      string   `json:"StartupCommand"`
}

// IsValid returns an error if the User struct is not valid
func (p *User) IsValid() (err error) {
	err = p.NameIsValid()
	if err != nil {
		return
	}
	err = p.UIDIsValid()
	if err != nil {
		return
	}
	/* err = p.PasswordIsValid()
	if err != nil {
		return
	} */
	err = p.PasswordExpiresDaysIsValid()
	if err != nil {
		return
	}
	return
}

// NameIsValid returns an error if the User name is empty
func (p *User) NameIsValid() (err error) {
	if p.Name == "" {
		return fmt.Errorf("invalid value for name (%s)", p.Name)
	}
	return
}

// UIDIsValid returns an error if the UID is outside bounds
// UIDs 1-999 are system users and 1000-60000 are normal users
// Bounds can be checked using:
// $grep -E '^UID_MIN|^UID_MAX' /etc/login.defs
func (p *User) UIDIsValid() (err error) {
	const (
		uidLowerBound = 0 // root user
		uidUpperBound = 60000
	)
	if p.UID != "" {
		uidNum, err := strconv.Atoi(p.UID)
		if err != nil || uidNum < uidLowerBound || uidNum > uidUpperBound {
			return fmt.Errorf("invalid value for UID (%s)", p.UID)
		}
	}
	return
}

// This function does not account for the Password key being intentionally
// unspecified versus set to blank
// PasswordIsValid returns an error if the User password is empty
/* func (p *User) PasswordIsValid() (err error) {
	if p.Password == "" {
		return fmt.Errorf("invalid value for Password (%s)", p.Password)
	}
	return
} */

// PasswordExpiresDaysISValid returns an error if the expire days is not
// within bounds set by the chage -M command
func (p *User) PasswordExpiresDaysIsValid() (err error) {
	const (
		noExpiration    = -1 //no expiration
		upperBoundChage = 99999
	)
	if p.PasswordExpiresDays < noExpiration || p.PasswordExpiresDays > upperBoundChage {
		return fmt.Errorf("invalid value for PasswordExpiresDays (%d)", p.PasswordExpiresDays)
	}
	return
}
