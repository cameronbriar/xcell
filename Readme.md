# How-to XCELL

# Install

Add this to your .bashrc

    alias xcell='python ~/home/user/xcell/xcell.py "$@"'

# Usage

    xcell <build|convert> [filename] -flag

## Flags
### Convert
    -s : Writes each cell even if blank or empty. (Default: ignore blanks/empty)

    Without this flag:

        # = Gender / Age                    # = Gender / Age
        Male    Age_1   inf                 Male|Age_1|inf
                Age_2   inf     becomes     Age_2|inf               <=== This row will not build correctly
        Female  Age_1   inf                 Female|Age_1|inf
                Age_2   inf                 Age_2|inf               <=== This row will not build correctly

    With this flag:

        # = Gender / Age                    # = Gender / Age
        Male    Age_1   inf                 Male|Age_1|inf
                Age_2   inf     becomes     |Age_2|inf               <=== This row will build correctly
        Female  Age_1   inf                 Female|Age_1|inf
                Age_2   inf                 |Age_2|inf               <=== This row will build correctly

### Build
    - There are no flags used when building.
