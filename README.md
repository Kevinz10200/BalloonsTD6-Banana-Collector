# BaloonsTD6-Banana-Collector
Uses periodic screencaps to identify banana farms, and automatically uses cursor to collect bananas.

Uses PyAutoGUI to take a screenshot of entire desktop, then openCV template matching to find potential locations of banana farms,
cash generating structures that require manual collection within a set amount of time. 

This potentially returns a ton of duplicate positions around single potential farm locations. This is bad because it will take longer
for the cursor to automatically move to collect, decreasing performance and increasing time which control is taken away from the player
while not accomplishing anything, increasing player frustration. 

Ideally the player would never notice this script running aside fromtheir banans being automatically collected.

Non-maximal suppression is then applied to reduce the amount of duplicates pointing to a single farm down to one coordinate.

PyAutoGUI then checks to see if any cursor input has been given by the player, if not, the player is assumed to be AFK and the cursor is
rapidly moved to farm locations after applying non-maximal suppression, collecting bananas. Finally the cursor is returned to the location
where it was found before collecting the first farm.

-Checking for player input means the script will not randomly hijack the cursor from the player while the player might be trying to perform
an action.

-Returning cursor to original location prevents cursors from being moved randomly, and the player can expect to find their cursor where they
left it after the split second the script takes to collect banans.
