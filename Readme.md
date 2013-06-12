# Install

Add this to your .bashrc

    alias xcell='python /home/user/xcell/xcell.py "$@"'

# Usage

    xcell <build|convert> [filename] -flag

    xcell build workbook.txt            # txt -> xls
    xcell convert workbook.xls [-s]     # xls -> txt

### Dependencies
The following Python packages are required: __xlwt__ and __xlrd__
    pip install xlwt
    pip install xlrd

### Flags

    -s    -    includes blank cells
    -c    -    set delimiter for column separation (default: |  )
    -n    -    set delimiter for sheet name        (default: -- )
    -e    -    set delimiter for end of sheet      (default: +  )
 
    -x    -    set underscore _ separated list of delimiters (default: |_--_+ )
    
    -o    -    prints to std.out
 
    Note:
          -x   overrides -c -n & -e
          -o   allows you to pipe result (e.g.    xcell build file.txt -o | vim -  )

          tab  to use TAB as a delimiter, simply use 'tab' as the keyword
               (e.g.   xcell build file.txt -x tab_--_+   )

          delimiters
               if you adjust the delimiters, you will need to account for them 
               each time you build or convert


## Examples

#### Times Table (table.txt)

    --times_table
    0|1|2|3|4|5|6|7|8|9|10
    1|1|2|3|4|5|6|7|8|9|10
    2|2|4|6|8|10|12|14|16|18|20
    3|3|6|9|12|15|18|21|24|27|30
    4|4|8|12|16|20|24|28|32|36|40
    5|5|10|15|20|25|30|35|40|45|50
    6|6|12|18|24|30|36|42|48|54|60
    7|7|14|21|28|35|42|49|56|63|70
    8|8|16|24|32|40|48|56|64|72|80
    9|9|18|27|36|45|54|63|72|81|90
    10|10|20|30|40|50|60|70|80|90|100
    +
    --times_table_mini
    3|2|1
    2|4|2
    1|2|1|woot
    +

     xcell build table.txt   # produces xcell.xls (XLS WORKBOOK)

    
    [0 ][1 ][2 ][3 ][4 ][5 ][6 ][7 ][8 ][9 ][10 ]
    [1 ][1 ][2 ][3 ][4 ][5 ][6 ][7 ][8 ][9 ][10 ]
    [2 ][2 ][4 ][6 ][8 ][10][12][14][16][18][20 ]
    [3 ][3 ][6 ][9 ][12][15][18][21][24][27][30 ]
    [4 ][4 ][8 ][12][16][20][24][28][32][36][40 ]
    [5 ][5 ][10][15][20][25][30][35][40][45][50 ]
    [6 ][6 ][12][18][24][30][36][42][48][54][60 ]
    [7 ][7 ][14][21][28][35][42][49][56][63][70 ]
    [8 ][8 ][16][24][32][40][48][56][64][72][80 ]
    [9 ][9 ][18][27][36][45][54][63][72][81][90 ]
    [10][10][20][30][40][50][60][70][80][90][100]

    [times_table]  <-- sheet 1
    

    [3 ][2 ][1 ]
    [2 ][4 ][2 ]
    [1 ][2 ][1 ][woot]
                  [times_table_mini]  <-- sheet 2

     xcell convert xcell.xls    # produces xcell.txt (TEXT FILE)


### Quota (quota.txt)

    --defines
    Child|Age.check('1-17')
    Adult|Age.check('18-120')
    Legend|Age.check('120+')
    Says_Yes_Often|Q1.yes and Q2.yes and Q3.yes and Q4.yes or (Q5.c1.all)|Positive Feelings
    Says_No_Often|not (condition.positive_feelings)
    Hero|Q6.lives_saved.count gt 5|Hero: Has saved more than  5 lives
    Passer_By|Q6.lives_saved.check('0-5')|Passer By:  * there is nothing here *
    item_1|plus|Situation 1
    item_2|plus|Situation 2
    item_3|plus|Situation 3
    item_4|plus|Situation 4
    item_5|plus|Situation 5
    item_6|plus|Situation 6
    item_7|plus|Situation 7
    item_8|plus|Situation 8
    item_9|plus|Situation 9
    item_10|plus|Situation 10
    +
    --experience
    # = Experience by Age
    Child|10000
    Adult|10000
    Legend|10000
    +
    --attitude
    # = Attitude by Choice 
    Says_Yes_Often|inf
    Says_No_Often|inf

    # = Attitude by Choice / Experience|Child|Adult|Legend
    Says_Yes_Often|inf|inf|inf
    Says_No_Often|inf|inf|inf
    +
    --hero
    # = Hero Status
    Hero|inf
    Passer_By|inf

    # = Hero Status by Experience|Hero|Passer_By
    Child|inf|inf
    Adult|inf|inf
    Legend|inf|inf

    # cells:10 = Hero by Situation|item_1|item_2|item_3|item_4|item_5|item_6|item_7|item_8|item_9|item_10
    Hero|inf|inf|inf|inf|inf|inf|inf|inf|inf|inf
    +


     xcell build quota.txt

     # open xcell.xls in your favorite editor (Libre Office Calc, Excel, ... )

     # if you run

     xcell convert xcell.xls

     # you get xcell.txt - an exact copy of quota.txt


### FLAG USAGE

     # going back to this from the Quota example
    
    # cells:10 = Hero by Situation|item_1|item_2|item_3|item_4|item_5|item_6|item_7|item_8|item_9|item_10
    Hero|inf|inf|inf|inf|inf|inf|inf|inf|inf|inf
    Passer_By|inf|inf|inf|inf|inf|inf|inf|inf|inf|inf
    +

    # you could have also written it as...

    # cells:10 = Hero by Situation
    Hero|item_1|inf
    |item_2|inf
    |item_3|inf
    |item_4|inf
    |item_5|inf
    |item_6|inf
    |item_7|inf
    |item_8|inf
    |item_9|inf
    |item_10|inf
    Passer_By|item_1|inf
    |item_2|inf
    |item_3|inf
    |item_4|inf
    |item_5|inf
    |item_6|inf
    |item_7|inf
    |item_8|inf
    |item_9|inf
    |item_10|inf
    +

    # when you build this 
    #   > xcell build quota.txt

    # everything is fine..

    # but when you convert it! - you need to pass the -s flag

    # (this accounts for the empty cells) - try it both ways and see the difference
    
### Fun Tips

    Use the VI editor
      - visual increment/decrement
      - yank/paste

    Use regular expressions

    :s,|.*,|inf,cg
    
    
### Disclaimer

     # because it would be
     # TERRIBLE to overwrite a file unintentionally
     # xcell always creates xcell.xls or xcell.txt

     # but if you want, pass the -f flag to write to the SAME FILENAME

     # For example: xcell build some_file.txt -f
     # Output: some_file.xls

     # not yet working

### Issues

    See Issues
