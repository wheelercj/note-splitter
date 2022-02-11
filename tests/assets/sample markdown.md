# sample markdown for regex tests

## full-line elements

#### empty line
```

    
\t
   \t   
\t   \t
```

#### not empty line
```
ksljdlfks
         .      
```

#### header
```
# first level header
## second level header
###### sixth level header
#      header surrounded with extra spaces   
### s8973#abc@#%
```

#### not header
```
#tag
##double-tag
> ##### quoted title
 # spaced title
    # indented title
a# letter in front of title
normal text
```

#### horizontal rule
Ignore the lines that have just a period in them.
```
---
.
----
.
----------------------------------------------------------------
.
  -       -   -
.
***
.
********************
.
*    **
.
___
.
___________________________
.
                     ___
```

#### not horizontal rule
```
--
-*_
--*
_ _
  *    *  
-a--
---         .
\---
```

#### frontmatter fence
```
---
***
```

#### not frontmatter fence
```
 ---
---\t
--- 
----
---a
.---
```

#### code fence
```optionalLanguage
your_code_here();
```

~~~
it_also_works_with_tildes();
~~~

#### not code fence
``
``
'``
'``
'''
a``
\``

#### math fence
```
$$
  $$  
\t$$\t
```

#### not math fence
```
$ $
.$$
$$b
$
$$$
```

#### blockquote
```
> this is a quote
> > this is a nested quote
>> this is also a nested quote
> 
>abc
>    extra spaces    
```

#### not blockquote
```
a> this is not a quote
< nope
```

#### to do
```
- [ ] unfinished
- [x] finished
    - [ ] indented
  - [ ]                
+ [ ]    with plus
* [ ] with asterisk
```

#### not to do
```
-[ ] 
- []  
- [ ]abc
```

#### footnote
```
[^1]: this is a footnote
[^footnote title with spaces]: footnote content
[^878]: 8379827843
```

#### not footnote
```
[2]: aksdf
[^ 3]: abc
[^4 ]: def
[ ^5]: ghi
[^6] jkl
[^7]:mno
[^^8]: pqr
(^9): stu
```

#### unordered list item
```
* with asterisk
- with minus
+ with plus
    * indented
        * indented again
-    with extra spaces    
+ 9837982738
```

#### not unordered list item
```
*unspaced
-- multiple minuses
= other symbols
\* escaped
a    * interrupted
```

#### ordered list item
```
1. these only allow numbers
2. not letters like a., b., c., etc.
    3. indented
        4. indented again
1. order and uniqueness don't matter
1) parenthesis instead of period
    3) indented
        4) indented again
198349831798. big number
387.     extra spaces        
0. zero
```

#### not ordered list item
```
a. no letters allowed
ii. same for Roman numerals
$. and special characters
1.unspaced
1)unspaced
1 .wrong space
1 . extra space
```

#### table divider
```
--- | --- | ---
|--- | --- | ---|
|:--- | ---: | :---:|
|:-- | --: | :-:| :--: |
|:---: | :---: | :---:|:---:|
|:--- | :--- | :--- |
|----------|:-------------:|------:|
------ | ------
```

#### not table divider
```
||
| -- |
\| --- |
| --- \|
| :- |
```

#### table row
```
|row1|row2|row3|
| row1 | row2 | row3 |
|8739 | 3879 | 38937|
|**bold**| `code` | |
| _italicized_ |
|\escaped|\||
| row1    | row 2 with <br /> a break tag |
| |
```

#### not table row
```
||

abc
| abc
abc |
abc || def
\| not \| a \| table \| row
```

## inline elements

#### tag
```
#tag
#spaced 
\t#tabbed\t
##double-tag
#with_underscore
#with-ending-hash#
#ümläuts
##中国人
#interrupted#tag ("#interrupted#" should match, but not the rest)
#interrupted@tag ("#interrupted" should match, but not the rest)
```

#### not tag
```
# header
\#escaped-tag
example.com/test#anchor-name
interrupted#word
!#negatedtag
```

#### file path in link
```
[](..\..\assets\comm-rota.pdf)
![](1e9b3e85368662b9d33d2fcd700cc84f.png)
[](file://C:\Users\chris\Documents\Essay.pdf)
[](C:/Users/chris/Documents/Essay.html)
[](C:\Users\chris\Documents\Advice.jpeg)
[account info](..\Other\account info.jpg)
![C:\Users\chris\Documents\Zettelkasten\assets\Screenshot_2020-05-27 2.png](C:\Users\chris\Documents\Zettelkasten\assets\Screenshot_2020-05-27 2.png)
![4d628bdda08ec00570422b0d030fd918.mp4](4d628bdda08ec00570422b0d030fd918.mp4)
[20200319163500.md](..\test docs\20200319163500.md)
[20200319163500.md](test docs/20200319163500.markdown)
```

#### not file path in link
It's okay to match some of these as long as the result is checked with `os.path.exists`.
```
`[20200319163500.md](test docs/20200319163500.markdown)`
[](c:\Users\chris\Documents\folder)
[](zotero://open-pdf/library/items/3PMYG2V7?page=7)
[abcdef@csun.edu](mailto:abcdef@csun.edu)
[wikipedia](wikipedia.org)
[](wikipedia.org/)
[](wikipedia.org/wiki)
[](www.wikipedia.org/wiki)
[](www2.wikipedia.org/wiki)
[](http://www.wikipedia.org)
[](https://www.wikipedia.org)
[](https://www.wikipedia.org/)
[](https://wikipedia.org/)
[](www.wikipedia.org/wiki/file.html)
[](www.wikipedia.org/wiki/file.htm)
[](wikipedia.org/wiki/file.html)
`[](wikipedia.org/wiki/file.html)`
```

#### time ID
```
29728398128922
83748937987224.md
2020738789739827384
0000000000000000
[[0000000389839823
083479387438973897]]
```

#### not time ID
```
[[20200911091623]]
2972839812892
329874387833a9837837387
```

## see also
* [Markdown Guide](https://www.markdownguide.org/basic-syntax)
* [Zettlr's regex test files](https://github.com/Zettlr/Zettlr/blob/develop/scripts/test-gui/test-files/Rendering/Miscellaneous%20Rendering%20Issues.md)
