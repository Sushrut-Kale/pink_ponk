from manim import *
import numpy as np
import random
class Pong(Scene):
    def construct(self):
        rect1 = Rectangle(height=2, width=0.2, color=BLUE).move_to(LEFT * 7)
        rect2 = Rectangle(height=2, width=0.2, color=BLUE).move_to(RIGHT * 7)
        self.add(rect1, rect2)
        t = 0
        def leftupdate(mob, dt):
            nonlocal t
            t += dt
            mob.set_y(np.sin(t * 2) * 2.2)
        def rightupdate(mob, dt):
            mob.set_y(np.sin(t * 2 + PI) * 2.2)
        rect1.add_updater(leftupdate)
        rect2.add_updater(rightupdate)
        ball = Circle(radius=0.5, color=WHITE).move_to(ORIGIN)
        ball.set_fill(GREEN_B, opacity=0.5)
        self.add(ball)
        velocity = np.array([3,2,0])
        reset_cooldown = 0
        def reset_ball():
            self.add_sound("game_end.mpeg")
            nonlocal velocity, reset_cooldown
            ball.move_to(ORIGIN)
            angle = random.uniform(-PI/3, PI/3)
            direction = random.choice([-1, 1])
            speed = 3.7
            velocity = np.array([
                direction * np.cos(angle) * speed,
                np.sin(angle) * speed,
                0
            ])
            reset_cooldown = 0.1
        def ballupdate(mob, dt):
            nonlocal velocity, reset_cooldown
            if reset_cooldown > 0:
                reset_cooldown -= dt
                return
            mob.shift(velocity * dt)
            if mob.get_top()[1] >= 3.5:
                velocity[1] *= -1
                self.add_sound("bounce.mpeg")
                mob.set_y(3.5 - mob.radius)
                mob.scale(0.8)
            if mob.get_bottom()[1] <= -3.5:
                velocity[1] *= -1
                self.add_sound("bounce.mpeg")
                mob.set_y(-3.5 + mob.radius)
                mob.scale(0.8)
            if (
                mob.get_right()[0] >= rect2.get_left()[0]
                and rect2.get_bottom()[1] <= mob.get_y() <= rect2.get_top()[1]
            ):
                velocity[0] *= -1
                self.add_sound("bounce.mpeg")
                mob.set_x(rect2.get_left()[0] - mob.radius)
                mob.scale(1.2)
            if (
                mob.get_left()[0] <= rect1.get_right()[0]
                and rect1.get_bottom()[1] <= mob.get_y() <= rect1.get_top()[1]
            ):
                velocity[0] *= -1
                self.add_sound("bounce.mpeg")
                mob.set_x(rect1.get_right()[0] + mob.radius)
                mob.scale(1.2)
            if mob.get_left()[0] > rect2.get_right()[0]:
                reset_ball()
            if mob.get_right()[0] < rect1.get_left()[0]:
                reset_ball()
        ball.add_updater(ballupdate)
        self.wait(20)
