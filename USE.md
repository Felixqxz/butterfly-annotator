# How to use Butterfly annotator?

## Initial setup
Now that the app is up and running, we can start setting the software for your data.

First things first, the only existing account by default goes by the username of "admin". Its password is editable in the `password.txt` file situated at the root of the project. *Whenever you will add a new dataset/"image bank", this account will be the only to have access to it*; it will have access to each and every image bank and its access is irrevocable. Note that, of course, other users can have access to banks as we will see in sections below.

### How to add a bank
Simply move your folder containing your data in the `banks/` folder at the root of the project. The name of the folder will be the name of the image bank. The folder should be discovered if you re-run the application. (It suffices to re-run the Flask back-end.) The structure that the folder should have is described in the section below. 

Otherwise, when you are on the home page of the application (where you can see "Your Banks"), you can drag and drop an archive containing the folder that holds your bank and upload it.

### How to organize your bank's folder
All files should be at the same level. Your folder should contain the images you want to annotate and their corresponding descriptions. To connect descriptions to images:
- If an image with filename `A.jpg` has a description only for itself, then the latter should be located in the file `A.txt`;
- If a group of images have the same description, then these images should all have a prefix (*containing no underscore*) in their filename, followed by *a single underscore*, itself followed by any text that does not **contain any other underscore**; that prefix that they all share should be the filename of their shared description. Thus `edelweiss_001.jpg, edelweiss_002.jpg, eldeweiss_backtothefuture.jpg` will all have the description contained in `edelweiss.txt`.

If 1. the description file does not exist, or 2. it contains an extra underscore, it will be ignored and not added to the image bank.

### How to format the description file
Only the *fourth line* of the file will be used. It should contain the entire description of the image(s) on that line.

### How to add other users to your image bank
First of all, the other user should create an account (possible very simply on the `Register` page when trying to log in). Then, supposing your account has the sufficient permission level on this bank, it suffices for you to go to the image bank, click on the `Accesses` tab and then `Add user`. Then, a modal window should open up to allow you to 1. choose the user you want to add (just type in their username), 2. their permission level.

### How do permissions work
There exists the following permission levels (they ranked by their level of power they have on a bank):
1. Super Admin: this role only exists for the aforementionned default 'admin' account; it has all permissions except that to remove itself from a bank;
2. Admin: this role has all permissions on the current bank: it can add/delete users to/from it, edit annotations;
3. Moderator: same as admin;
4. Editor: can only edit annotations;
5. Viewer: can only view annotations.
From moderator to super admin, the difference is that a role allows to add/delete users that are lower hierarchically in that bank's permission organization---so a moderator can only add/delete editors/viewers, for instance.

## Annotating images

### How to annotate an image
Supposing you have the permission to, it suffices to open up the bank in which you want to edit your image, find the image, click on it. Then, you can simply draw polygons by clicking on where you want to place points. Finally, in the lower part, you can select text bits of the description that you want to associate your polygonal region with; to finish it, click back to the first point that you have drawn. You might first want to start by selecting relevant bits, and then only starting to draw polygonal shapes, so that you can associate the region to the text all at once.

Note that there will be automatically generated suggestions (in grey) for you to annotate your images even faster. When you are done, **don't forget to save!** Any change must be saved.

### Annotation view features
- Holding `Shift` and clicking "close enough" to a polygon will delete it;
- You can undo adding/deleting a polygon with `Ctrl + Z` and redo with `Ctrl + Y`;
- You can cancel your last point in your current polygonal region by re-clicking on it;
- You can move points of polygons by simply hovering them, and then dragging them to the position you want.

### Important behaviours
- Deleting a polygon that's associated to a text bit and saving, will delete the text bit;
- Deleting a text bit that's associated to a polygon and saving, will delete the polygon;
- Having at least one annotation on an image disables the suggestions.

## Downloading the annotated data
Easy! Get back to the list of bank's images (where you can also handle accesses). You can notice that the last tab says "Export to JSON": click on it, and you will be offered to download a JSON file containing all the annotations.
