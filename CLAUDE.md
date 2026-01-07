# The Farmer Was Replaced - 基本ルール

## 参照先
- `__builtins__.py` に全ての定義（Items, Entities, Unlocks, 関数など）がある

## 作物コスト
`get_cost(entity)` で取得すること。ハードコーディング禁止。
例: `get_cost(Entities.Pumpkin)` → `{Items.Carrot: 1}`

## 作物 → アイテム
| Entity | Item |
|--------|------|
| Grass | Hay |
| Bush | Wood |
| Tree | Wood |
| Carrot | Carrot |
| Pumpkin | Pumpkin |
| Sunflower | Power |

## 特殊ルール
- **Tree**: 隣にTreeがあると成長が遅い → Grassと市松模様に配置
- **Pumpkin**: 正方形で収穫すると効率UP（隣接でまとめて収穫、数の3乗）
- **Sunflower**: 花びら最大 + 10本以上で5倍ボーナス

## 地面
- `Grounds.Grassland`: Grass, Bush, Tree用
- `Grounds.Soil`: Carrot, Pumpkin, Sunflower, Cactus用（`till()`で切替）

## 定数
- マジックナンバーは `const.py` に定義すること
