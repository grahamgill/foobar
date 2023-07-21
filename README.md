# Google foobar solutions

## Level 1
* `bunnyid.py`

      bunnyid(x: int, y: int)
    Enumerate the $\mathbb N^2$ lattice points along diagonals `x + y = n`
    of increasing 1-norm distance `n` from the origin `(0,0)` in $\mathbb Z^2$.
    Counting should increase with distance along the horizontal axis.

    E.g., count
    ```
    | 7
    | 4 8
    | 2 5 9
    | 1 3 6 10
    ----------
    ```
    from:
    ```
    (1,1) => 1
    (1,2) => 2
    (2,1) => 3
    (1,3) => 4
    (2,2) => 5
    (3,1) => 6
    (1,4) => 7
    (2,3) => 8
    (3,2) => 9
    (4,1) => 10
    ```

    Stringify the return result. `x` and `y` are guaranteed to be `int`s in the range 1 to 100000.
