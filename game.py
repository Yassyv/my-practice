#時はクリスマスの夜、サンタさんが子供たちにプレゼントをばら撒くゲーム「サンタシューティング」へようこそ
#あなたはサンタさんです。スペースキーで子供たちにプレゼントを投げることができます
#子供にはいい子供と悪い子供がいます。悪い子供にはプレゼントをあげるなとサンタ大魔王から言われているので、気をつけましょう。
#いい子供にプレゼントをあげると+1pt、悪い子供にプレゼントをあげると-5ptです。
#サンタさんは子供に存在をバレてはいけません。ぶつかったら一発でアウトです！！！
#ただ、お利口に寝ている子供達(=いい子供)もいます。寝ている子どもはぶつかっても問題ありません。




from random import random
import pyxel


######################
## 各種設定値
SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

STAR_COUNT = 100
STAR_COLOR_HIGH = 6
STAR_COLOR_LOW = 10

PLAYER_WIDTH = 10
PLAYER_HEIGHT = 12
PLAYER_SPEED = 2

BULLET_WIDTH = 8
BULLET_HEIGHT = 8
BULLET_COLOR = 11
BULLET_SPEED = 4

ENEMY_WIDTH = 8
ENEMY_HEIGHT = 8
ENEMY_SPEED = 1.5

BAD_WIDTH = 8
BAD_HEIGHT = 8
BAD_SPEED = 2

SLEEP_WIDTH = 8
SLEEP_HEIGHT = 8
SLEEP_SPEED = 0.7


BLAST_START_RADIUS = 1
BLAST_END_RADIUS = 8
BLAST_COLOR_IN = 5
BLAST_COLOR_OUT = 15


enemy_list = []
bullet_list = []
blast_list = []
bad_list = []
sleep_list = []


def update_list(list):
    for elem in list:
        elem.update()


def draw_list(list):
    for elem in list:
        elem.draw()


def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
        else:
            i += 1


######################
## 背景画像クラス
class Background:
    def __init__(self):
        self.star_list = []
        for i in range(STAR_COUNT):
            self.star_list.append(
                (random() * pyxel.width, random() * pyxel.height, random() * 1.5 + 1)
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.star_list):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.star_list[i] = (x, y, speed)

    def draw(self):
        for (x, y, speed) in self.star_list:
            pyxel.pset(x, y, STAR_COLOR_HIGH if speed > 1.8 else STAR_COLOR_LOW)

######################
## プレイヤークラス
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.alive = True




    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_UP):
            self.y -= PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += PLAYER_SPEED

        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - self.h)

        if pyxel.btnp(pyxel.KEY_SPACE):
            Bullet(
                self.x + (PLAYER_WIDTH - BULLET_WIDTH) / 2, self.y - BULLET_HEIGHT / 2
            )

            pyxel.play(0, 0)
        pyxel.load("my_resource.pyxres")


    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 0)


######################
## プレゼントクラス
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.alive = True

        bullet_list.append(self)

    def update(self):
        self.y -= BULLET_SPEED

        if self.y + self.h - 1 < 0:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 1, 0, 0, self.w, self.h, 0)

######################
## いい子供たち
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.dir = 1
        self.alive = True
        self.offset = int(random() * 60)

        enemy_list.append(self)

    def update(self):
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.x += ENEMY_SPEED
            self.dir = 1
        else:
            self.x -= ENEMY_SPEED
            self.dir = -1

        self.y += ENEMY_SPEED

        if self.y > pyxel.height - 1:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 2, 0, 0, self.w * self.dir, self.h, 0)

######################
## 悪い子供たち
class Bad:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BAD_WIDTH
        self.h = BAD_HEIGHT
        self.dir = 1
        self.alive = True
        self.offset = int(random() * 60)

        bad_list.append(self)

    def update(self):
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.x += BAD_SPEED
            self.dir = 1
        else:
            self.x -= BAD_SPEED
            self.dir = -1

        self.y += BAD_SPEED

        if self.y > pyxel.height - 1:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 2, 8, 0, self.w * self.dir, self.h, 0)

######################
## 寝ている子供たち
class Sleep:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = SLEEP_WIDTH
        self.h = SLEEP_HEIGHT
        self.dir = 1
        self.alive = True
        self.offset = int(random() * 60)

        sleep_list.append(self)

    def update(self):
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.x += SLEEP_SPEED
            self.dir = 1
        else:
            self.x -= SLEEP_SPEED
            self.dir = -1

        self.y += SLEEP_SPEED

        if self.y > pyxel.height - 1:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 2, 0, 8, self.w * self.dir, self.h, 0)


######################
## 爆発画像クラス
class Blast:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BLAST_START_RADIUS
        self.alive = True

        blast_list.append(self)

    def update(self):
        self.radius += 1

        if self.radius > BLAST_END_RADIUS:
            self.alive = False

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, BLAST_COLOR_IN)
        pyxel.circb(self.x, self.y, self.radius, BLAST_COLOR_OUT)

######################
## シューティングゲームアプリの本体を宣言するクラス
class App:
    def __init__(self):
        pyxel.init(120, 160, caption="Santa Shooter")

        ## 自分の機体の描画

        ## 音声のセット
        pyxel.sound(0).set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sound(1).set("a3a2c2c2", "n", "7742", "s", 10)

        ## その他設定
        self.scene = SCENE_TITLE        ## ゲームの状態をもたせる変数
        self.score = 0
        self.mscore = 0                ## 得点
        self.background = Background()  ## 背景画像をセット
        self.player = Player(pyxel.width / 2, pyxel.height - 20)

        ## ゲームの本体（updateとdraw）
        pyxel.run(self.update, self.draw)


    ###############################
    # ゲームの本体 その１
    def update(self):

        ## もし[Q]ボタンが押されていたらゲーム終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        ## 背景画像を更新
        self.background.update()

        ## ゲームの状態を判定
        if self.scene == SCENE_TITLE:       #### タイトル画面の場合
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:      #### ゲーム中の場合
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:  #### ゲームオーバー画面の場合
            self.update_gameover_scene()

    #### タイトル画面の場合
    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene = SCENE_PLAY

    #### ゲーム中の場合
    def update_play_scene(self):

        ## フレームカウントの回に１回の頻度で敵キャラが発生
        if pyxel.frame_count % 30 == 0:
            Enemy(random() * (pyxel.width - PLAYER_WIDTH), 0)
        ## フレームカウントの回に１回の頻度で敵キャラが発生
        if pyxel.frame_count % 50 == 0:
            Bad(random() * (pyxel.width - PLAYER_WIDTH), 0)
        ## フレームカウントの回に１回の頻度で敵キャラが発生
        if pyxel.frame_count % 20 == 0:
            Sleep(random() * (pyxel.width - PLAYER_WIDTH), 0)

        ## 敵キャラとプレゼントの当たり判定
        for a in enemy_list:
            for b in bullet_list:
                if (
                    a.x + a.w > b.x
                    and b.x + b.w > a.x
                    and a.y + a.h > b.y
                    and b.y + b.h > a.y
                ):
                    a.alive = False
                    b.alive = False

                    blast_list.append(
                        Blast(a.x + ENEMY_WIDTH / 2, a.y + ENEMY_HEIGHT / 2)
                    )

                    pyxel.play(1, 1)

                    self.score += 1
        ## 悪い子供とプレゼントの当たり判定
        for a in bad_list:
            for b in bullet_list:
                if (
                    a.x + a.w > b.x
                    and b.x + b.w > a.x
                    and a.y + a.h > b.y
                    and b.y + b.h > a.y
                ):
                    a.alive = False
                    b.alive = False

                    blast_list.append(
                        Blast(a.x + BAD_WIDTH / 2, a.y + BAD_HEIGHT / 2)
                    )
                    pyxel.play(1, 1)

                    self.score -= 5
        ## 寝ている子供とプレゼントの当たり判定
        for a in sleep_list:
            for b in bullet_list:
                if (
                    a.x + a.w > b.x
                    and b.x + b.w > a.x
                    and a.y + a.h > b.y
                    and b.y + b.h > a.y
                ):
                    a.alive = False
                    b.alive = False

                    blast_list.append(
                        Blast(a.x + SLEEP_WIDTH / 2, a.y + SLEEP_HEIGHT / 2)
                    )

                    pyxel.play(1, 1)

                    self.score += 1



        ## 敵キャラとプレイヤーの当たり判定
        for enemy in enemy_list:
            if (
                self.player.x + self.player.w > enemy.x
                and enemy.x + enemy.w > self.player.x
                and self.player.y + self.player.h > enemy.y
                and enemy.y + enemy.h > self.player.y
            ):
                enemy.alive = False

                # 自機の爆発を生成する
                blast_list.append(
                    Blast(
                        self.player.x + PLAYER_WIDTH / 2,
                        self.player.y + PLAYER_HEIGHT / 2,
                    )
                )
                pyxel.play(1, 1)

                ## 敵キャラと接触して爆発したらゲームオーバー画面に
                self.scene = SCENE_GAMEOVER
        ## ダメな子供とプレイヤーの当たり判定
        for bad in bad_list:
            if (
                self.player.x + self.player.w > bad.x
                and bad.x + bad.w > self.player.x
                and self.player.y + self.player.h > bad.y
                and bad.y +bad.h > self.player.y
            ):
                bad.alive = False

                # 自機の爆発を生成する
                blast_list.append(
                    Blast(
                        self.player.x + PLAYER_WIDTH / 2,
                        self.player.y + PLAYER_HEIGHT / 2,
                    )
                )
                pyxel.play(1, 1)

                ## ダメな子供と接触して爆発したらゲームオーバー画面に
                self.scene = SCENE_GAMEOVER

        ## 画面に表示するオブジェクトを更新
        self.player.update()
        update_list(bullet_list)
        update_list(enemy_list)
        update_list(blast_list)
        update_list(bad_list)
        update_list(sleep_list)


        cleanup_list(enemy_list)
        cleanup_list(bullet_list)
        cleanup_list(blast_list)
        cleanup_list(bad_list)
        cleanup_list(sleep_list)


    #### ゲームオーバー画面の場合
    def update_gameover_scene(self):
        update_list(bullet_list)
        update_list(enemy_list)
        update_list(blast_list)
        update_list(bad_list)
        update_list(sleep_list)

        cleanup_list(enemy_list)
        cleanup_list(bullet_list)
        cleanup_list(blast_list)
        cleanup_list(bad_list)
        cleanup_list(sleep_list)
        ## スペースキー押されたら再ゲーム
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width / 2
            self.player.y = pyxel.height - 20
            self.score = 0


            enemy_list.clear()
            bullet_list.clear()
            blast_list.clear()
            bad_list.clear()
            sleep_list.clear()

    ###############################
    # ゲームの本体 その２
    def draw(self):
        ## 一度塗りつぶす
        pyxel.cls(0)

        ## 背景画像の描画
        self.background.draw()

        ## ゲームの状態を判定
        if self.scene == SCENE_TITLE:       #### タイトル画面の場合
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:      #### ゲーム中の場合
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:  #### ゲームオーバー画面の場合
            self.draw_gameover_scene()

        ## 得点の表示
        pyxel.text(39, 4, f"present {self.score:5}", 7)


    #### タイトル画面の場合
    def draw_title_scene(self):

        pyxel.text(35, 66, "Santa Shooter", pyxel.frame_count % 16)
        pyxel.text(31, 126, "- PRESS SPACE -", 13)

    #### ゲーム中の場合
    def draw_play_scene(self):
        ## プレイヤーの機体、弾丸、敵キャラ、爆発を表示
        self.player.draw()
        draw_list(bullet_list)
        draw_list(enemy_list)
        draw_list(blast_list)
        draw_list(bad_list)
        draw_list(sleep_list)

    #### ゲームオーバー画面の場合
    def draw_gameover_scene(self):
        ## 残っている弾丸、敵キャラ、爆発を表示
        draw_list(bullet_list)
        draw_list(enemy_list)
        draw_list(blast_list)
        draw_list(bad_list)
        draw_list(sleep_list)
        ## ゲームオーバー文字と再ゲームを促す文字を表示
        pyxel.text(11, 66, "You got caught by a child", 8)
        pyxel.text(31, 126, "- PRESS SPACE -", 13)

## プログラムの宣言ここまで
##################################################


App()

#
# このソースコードは
# Appクラスを呼び出すだけのシンプルなプログラム
