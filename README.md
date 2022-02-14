# Bomberman pygame application day 1

- Read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before start
- [Pygame primer](https://realpython.com/pygame-a-primer/#sprite-groups)
- [Pygame sprites and groups](https://kidscancode.org/blog/2016/08/pygame_1-2_working-with-sprites/)

You already have initial structure of game Bomberman.

<img width="500" alt="Initial" src="https://user-images.githubusercontent.com/80070761/153867128-3e78f7d2-1231-46f2-8e8a-af35caa03e24.png">

There are `player` (green rectangle) and `walls` (white squares).
You should implement these features:
- Player must be able to move up, down, left, right when user
presses arrows (overwrite method update).
- Player cannot walk away from field and walk over the walls.
- Player should deploy a bomb when user presses space key. Player cannot
put bomb if less than 1 second has passed from last deploying (that is
all so far, bomb will explode later). Player cannot walk over the bomb also.
- Replace simple colored rectangles with pictures given in `"app/images/`.

Also, it is bad idea to store full application logic in `main.py`. 
- Implement your architecture ideas

**Hint**: it will be good to have a class that stores and handles 
such things as: `clock`, `screen`, `running`, `events`, `groups` etc.
If sprites store link to this class, they can interact with these
things in methods instead of module level.

![Example](https://user-images.githubusercontent.com/80070761/153866858-de575692-0b47-4a29-97cd-4326fde4dbb0.gif)
