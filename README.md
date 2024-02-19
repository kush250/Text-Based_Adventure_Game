# Text-Based Adventure Game                                                          

Implemented a game engine which would load game maps and let players play a game by updating the state of the game world. Used Python and extended game versions where players could win/lose depending on items they are carrying and room they are in.


## A list of the three extensions for the Adventure Game

I implemented the below extensions for the game-

1)	A drop verb: 

	-	The drop verb does exactly opposite of what the get verb does. It sees if an item is present in the inventory or not, if it is there, it removes the item from the inventory list and adds the item in the current room that we are in (i.e the present_room) printing a message saying- You drop the item <item_name>. 

	-	If the item that we used with the drop verb is not present in the inventory that it will print a message that says that the player is not carrying this item in inventory.

	-	If the length of the arguments used with the drop verb are are not one, then it will print a message saying that the player has to drop something. 

	-	If more than one item's prefixes match with the specified item, then my code will give options as to which item did the user specified to drop.



2)	Abbreviations for verbs, directions, and items: 

	-	This is when we dont want to waste enough time and effort while writing a command and want the system to quickly recognise from the set of available options of which verb, direction and items are we referring to. An example of this would be inventory as the professor gave. If we write 'i' or 'inv' or 'inve' or the whole word inventory, it should match it with the existing word that the game knows, i.e. inventory and should list out the current inventory that the player holds.

	-	On the other case, if we write g, then we have two verbs like go and get therefore the game should give the option of choosing between the two and proceed thereby.

	-	This also handles cases where we have matched a whole word but still have other words which have prefix as this word. In this case, the game should directly get the whole word instead of listing those options because otherwise we wont be able to get the whole word ever and this would be an endless loop.
   	
	- 	Also, for items/direction, we support consists method too (include matching). Like, en should provide option for pen, pencil, complen as each word having en in it. This is also handled for items/directions.

	-	The system also understands when we write 'ge te' that we are referring to get ten if ten was the only  in the present room and there are no other verbs starting with ge other than get.


3)	Help: 

	-	The help keyword helps us to know of all the verbs that are in the game. Whenever we do help, it will print all the verbs like: go, get, drop and look. Any new verbs that are introduced will be added in our total verb list. 

	-	Because of help, it is useful to players to know of all the verbs in the game and get aware of what each verb does. We have also added description in all the verbs what they do therefore the players will be easily able to play the game.




## An example of a difficult issue or bug and how you resolved- 
-	While writing code for abbreviations as verbs extension, I was not able to fetch a particular prefix of the word following the verb when there were multiple items with same prefix. The code was breaking there and when I resolved that, another issue came where if a word was a exact match and a still a prefix like other items in the dictionary, get would not work. For example if there were items like ten, tencent and tener; when I did get ten, it would ask for choices between those three words instead of just getting ten as it was exact match! Then I found a solution for it and got it working.


   	
## How I tested my code-
-	Initially I would write a function and then test it in local. Then as I wrote more functions, I would see if all the code was working well with other functions. So did sort of continuous integration on my code to test its overall functionality.

-	Then I imported the demo test files like loop.map and ambig.map that were given in the document and initially tried testing on them. I made sure that I was considering all the test cases especially the edge ones and making sure the game engine was giving expected output on them. I played around more with the abbreviation extension to see if all prefixes were correctly getting extracted and matched with the verbs of our map. I also tried to make sure the extensions were working thoroughly without compromising the baseline behaviour.

   
 (I spent roughly 30 hours working on this project)
