# my-practice
PythonライブラリのPyxelを用いたゲームです

• ゲームのコンセプト 
クリスマスの夜、サンタさんが子供に見つからないようにプレゼントをシューティングしていく。子供たちの中には寝ている子供(⻘色の帽子をかぶっている)と起きている子供 (金髪、茶髪の子供)が存在する。起きている子供にサンタさんが当たってしまうと正体がバレるので即ゲームオーバー。寝ている子供に当たる分には何も起こらない。また子供たちの中にはいい子供(⻘色の帽子、茶髪)と悪い子供(金髪)が存在する。いい子供に はプレゼントをあげるべきなので、当てたら1ptが加算されるが、悪い子供にはプレゼントをあげてはいけないので5pt減る。子供に見つからずに、1人でも多くのいい子供にプレゼントを配ろう!!

• ファイル構成
game.py と my_resource.pyxres で構成される

• ゲーム開始方法
game.py を実行する。

• 操作方法
子供たちがオート画面上部から下部に向かって、左右に揺れながら移動してくる。
サンタさん(プレイヤー)は矢印キーで移動でき、スペースキーで子供たちにプレゼ ントをシュートできる サンタさんが起きている子供と接触するとゲームオーバーとなる。
