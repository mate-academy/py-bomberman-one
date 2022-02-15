# Bomberman pygame application day 1

- Read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before start
- [Pygame primer](https://realpython.com/pygame-a-primer/)
- [Pygame sprites and groups](https://kidscancode.org/blog/2016/08/pygame_1-2_working-with-sprites/)

Games! Games are a perfect example to show OOP principles at work.
You could play the game Bomberman in your youth or childhood, now
it is time to write your own a little modified version.
You already have an initial structure of the game Bomberman.

![Example](https://user-images.githubusercontent.com/80070761/153867128-3e78f7d2-1231-46f2-8e8a-af35caa03e24.png)

There are `player` (green rectangle) and `walls` (white squares).
You should implement these features:
1. Player movements. The player should be able to move left, right, up, down.
Sprites `update` method is called every frame, so use `self.rect.move_ip`
the method inside `update` to move the player. Movement direction depends
on the pressed key by the user. Use `pygame.key.get_pressed` to get the keys that are
currently pressed. Use arrows to move the player. [Player](https://realpython.com/pygame-a-primer/#sprites)
2. Player cannot walk away from the field. Use player's `self.rect.left`,
`self.rect.right`, `self.rect.top`, `self.rect.bottom` - coordinates of player
borders and compare them to field borders `SCREEN_WIDTH`, `SCREEN_HEIGHT`.
If the player coordinate is out of bound, it should change it to field border.
3. Player cannot walk over the walls. Walls are stored in group `walls`.
Use `pygame.sprite.spritecollideany` with the player and walls group 
to check if the player is colliding with any sprite in that group. (If after 
`self.rect.move_ip` player starts colliding - just move it back). [Collision detection](https://realpython.com/pygame-a-primer/#collision-detection)
4. Player should plant the bomb when the user presses the space button. 
Implement class `Bomb` that should be a sprite. Bomb should be planted on the 
current player's coordinates. But the player
cannot walk over the bomb, think about how the player gets off the bomb after the
planting.
5. Player cannot put bomb if less than 1 second has passed from last planting 
(the logic of the explosion you will implement later). There are `60` frames per second.
You can store timeout in the attribute and reduce it in `update` method.
6. Replace simple colored rectangles with images given in `"app/images/`. Use
`pygame.image.load("source.png").convert_alpha()` instead of `Surface`. The player
image should change when he goes in different directions.[Sprite images](https://realpython.com/pygame-a-primer/#sprite-images)

All information you can find in guides links on the top of the tasks.

Also, it is a bad idea to store full application logic in `main.py`. 
- Implement your architecture ideas

**Hint**: it will be good to have a class that stores and handles 
such things as: `clock`, `screen`, `running`, `events`, `groups` etc.
If sprites store link to this class, they can interact with these
things in methods instead of module level.

![Example](https://user-images.githubusercontent.com/80070761/153866858-de575692-0b47-4a29-97cd-4326fde4dbb0.gif)