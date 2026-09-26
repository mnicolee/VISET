# Notes from going through the current eunoia package (version 0.6.0)


### ITEM 1: Glyph, Label, Line overlap
At the default figure size, the set labels ("Atorvastatin", "Simvastatin") can sit on top of the packed member names, even though the member boxes should avoid the labels.

Changing `figsize` and `fontsize` can make this more obvious. At figure size = (15, 3), two circles push their labels outside with leader lines, but Sunitinib does not, so its label sits on top of the names and becomes unreadable. Sunitinib (35) may be getting more usable area than Atorvastatin (35, 12 shared) and Simvastatin (32, 12 shared), which could be why its label stays inside.

At figure size = (15, 3), the leader lines also run through the packed names. The line starts from the centre of the region by default, so it goes through the names before reaching the label. `labels={"placement": {"tether": "boundary"}}` starts the line at the edge of the circle instead, which looks cleaner. It may make sense for `boundary` to be the default when names are shown inside the regions.

![15x3](images/A2%20set%20of%203_Fig%20size%2015%20and%203.png)
![15x5](images/A2%20set%20of%203_Fig%20size%2015%20and%205.png)
![gene names overlap](images/Gene%20names%20overlap_B.png)

### ITEM 2: Space rearrangement
Same code and seed, with only `figsize` changed.

**The size difference between labels and member names changes with `figsize`.** At figure size = (15, 8), the set labels and member names are already quite similar in size. At larger figure sizes, the difference stays small.

From what I read in the package, the member names are set to `9pt × k` (`k` is auto-picked, capped at 1, floor of 0.35), while labels stay fixed at 11pt. This means the member names shrink at smaller figure sizes, but once `k` reaches 1 they stay at 9pt while the labels stay at 11pt. One option could be to scale the labels with `k` as well, while keeping a fixed ratio between labels and names, for example labels at `14k` vs names at `9k`. A minimum label size would probably still be needed so labels do not get too small. Since the label itself is also an obstacle for member placement, its size would feed back into `k` too.

![15x8](images/A2%20set%20of%203_Fig%20size%2015%20and%208.png)

### ITEM 3: `mode="list"` layout, columns and outside-list overlaps
In list mode, all names for a region are stacked one per line as a single block. If the whole block fits, it stays inside. Otherwise it gets moved outside with a leader line.

At figure size = (15, 15), all four lists are too tall and get pushed outside. The circles then shrink into a small cluster in the middle and the page becomes quite busy.

It might work better if the list could wrap into 2 to 3 shorter columns once one column becomes too tall. That would use the available horizontal space and could keep more names inside at a readable size.

![list 15x15](images/A2%20mode_list_15x15.png)
![list max 10](images/A2%20mode_list_max10_15x15.png)

![list 12x12](images/Sample%20B3%20genes%20list%2012x12.png)

**Possible `columns` arrangement:**
- A multiple `columns` arrangement with the number of columns determined by the maximum number of words to fit per row.

With a dataset that has longer names, some lists no longer fit inside the circles and get moved outside. Once that happens, a few cross-overs start to appear such as neighbouring lists can run into each other, or intersection lists sit quite close to the circles and can be crossed by leader lines or other lists. This may be related to the outside-list layout being re-measured for a fixed number of rounds. If it stops after four rounds, the final text can still end up larger than what the earlier placement was based on.

Of course, the overlap can be solved by increasing the figure size, but the issue is that it then leaves a lot of white space, which is undesirable, when the lists might have been rotated better.

The set label is also on the top line of the list at the same size as the member names, so it becomes difficult to distinguish once the layout gets crowded. 

### ITEM 4: Longer names get squeezed into a few long rows
**Names seem to fill horizontally before making use of the vertical space.** At figure size = (15, 15), the names stretch into long rows while there is still a lot of unused space above and below, which makes the layout look a bit squashed. At figure size = (10, 10), the smaller circles pack the names more tightly and it looks better, although more stacked rows would still be easier to read. 

![15x15](images/A2%20set%20of%203_Fig%20size%2015%20and%2015.png)

![10x10](images/Sample%20B1%20genes%20packed%2010x10_2.png)
![20x20](images/Sample%20B2%20genes%20packed%2020x20.png)
![square list 35x35](images/Square%20shape_listmode.png)

With a dataset that has longer names, the names get squeezed into a few long rows across the middle of each circle. The font becomes very small even though there is still a lot of empty space above and below.

Even at figure size = (20, 20), which is a very large figure, it still stays at one or two rows with several long names on each row.

It seems like the font could potentially stay larger if the names were allowed to spread across more rows instead of fitting as many as possible into each row.

I noticed something similar in `mode="list"` using the square shape. Even at figure size = (35, 35), both the member names and labels are still quite small. I would have expected the text to scale up more with the figure size.

There are already kwargs to control this manually, e.g. `members={"mode": "list", "fontsize": 20}` and `labels={"fontsize": 28}`, so this is more about the defaults and how much manual tuning is needed. Increasing the font size can also help with the row layout because fewer names fit per row, so the names naturally spread over more rows.

I also noticed that when the font size is pushed too high, the label starts overlapping the members (as mentioned in Item 1) and the members in the intersection can disappear. In the example below, all three intersecting members disappear together rather than only the one that no longer fits.

### ITEM 5: Three-way overlap is missing with `shape="circle"`
Atorvastatin, Simvastatin and Sunitinib share 2 genes, `CYP3A4` and `NR1I2`. With the default `shape="circle"`, there is a three-way intersection, but these 2 genes do not appear in it even though they should be there.

The other shapes I tried, ellipse, square, rectangle and rotated rectangle, all show `CYP3A4` and `NR1I2` in the three-way overlap.

![circle](images/Circle%20overflow.png)
![ellipse](images/Ellipse%20overflow.png)
![square](images/Square%20overflow.png)
![rectangle](images/Rectangle%20overflow.png)
![rotated rectangle](images/RotatedRectangle%20overflow.png)

### ITEM 6: Different fonts can change how many members fit
With the same code and seed, switching between fonts such as IBM Plex Mono, Inter and the default DejaVu Sans resulted in a different number of members being left out. I only saw this when the figure was already very constrained, for example at figure size = (15, 3), but it means the exact font choice can affect which members still fit in the layout.

### ITEM 7: Plotly title is hidden with the default margins
With the default `plot_plotly()`, a title added with `fig.update_layout(title=...)` does not show because all margins are set to 0. It appears once I add some top margin, e.g. `fig.update_layout(title="...", margin={"t": 50})`. Maybe the default could leave a little room at the top, or there could be a `title` option, so adding a title does not require a separate margin adjustment.
