.. raw:: html

    %path = "Mathematik/Funktionen/exponentiell"
    %kind = kinda["Übungen"]
    %level = 11
    <!-- html -->

.. role:: asis(raw)
    :format: html latex

Basics
------

In der **exponentiellen Funktion**

.. math::

    y = a^x

nennen wir

- `x` den **Exponenten**
- `a` die **Basis**
- `y` die **exponentielle Funktion** von `x` zur Basis `a`

Der **Exponent** sagt wie oft die *Multiplikation* mit `a` wiederholt wird.
`a` muss eine positive reelle Zahl sein : `a\in\mathbb{R}`.

.. note::

    Multiplikation ist eine Operation der realen Welt, die als
    Zahl codiert wird. In der Zahlenmenge `\mathbb{Q}`
    ist die Operation Teil der Zahl: `2` meint `\cdot 2` und `1/2` meint `/2`.
    Das Zeichen `\cdot` steht für die Multiplikation und `/` steht für die umgekehrte (inverse)
    Operation, die Division, welche mit der Einbindung der Brüche in `\mathbb{Q}` Teil der Zahl wurde.
    Also sprechen wir nur mehr von Multiplikation und meinen die Anwendung
    der Operation aus `\mathbb{Q}\subset\mathbb{R}`.

Wenn `a` größer als `1` ist, dann wächst `y` mit `x` *strikt monoton*: `x_1<x_2 \Rightarrow y_1<y_2`.

.. tikz:: \begin{axis}[grid=both,axis lines=middle,xmin=-3,xmax=3,ymin=0,ymax=8, samples=50]
     \addplot[green]  {pow(2,x)} node[above]{$y=2^x$};
    \end{axis}

Wenn `a` kleiner als `1` ist, dann fällt `y` mit `x` *strikt monoton*: `x_1<x_2 \Rightarrow y_1>y_2`.

.. tikz:: \begin{axis}[grid=both,axis lines=middle,xmin=-3,xmax=3,ymin=0,ymax=8, samples=50]
     \addplot[green]  {pow(1/2,x)} node[above]{$y=(\frac{1}{2})^x$};
    \end{axis}


Diskussion
----------
    
Vergleichen wir die Anzahl der Wertekombinationen von `n` bits:

.. math::
    
    2^n

mit dem Wachstumsprozess, wie etwa das Anwachsen des Kapitals mit der jährlichen Verzinsung

.. math::

    (1+\frac{i}{100})^n

oder das besonders interessante natürliche Wachstum

.. math::

    e^x = \lim_{n->\infty}(1+\frac{1}{n})^{nx} = \lim_{m->\infty}(1+\frac{x}{m})^m


Der Schlüssel zum Vestehen der Gemeinsamkeiten steckt im Interpretieren von **Information** in der Form von Bits als Wachstumsprozess.
Jedes Bit vergößert mit `1` mal der vorhandenen Anzahl von Wertekombinationen.
Notieren wir diesen Aspekt des Bits mit `(1+1)`, um zu betonen, dass `1` dazu kommt.
Die Klammern machen den Ausdruck zu einem Operator, einem Element der Zahlenmenge `\mathbb Q`.
`n` wiederholte Anwendungen von `(1+1)` erzeugen eine Vielzahl der Größe

.. math::

    (1+1)^n = 2^n

Jedes Bit wird zur bestehenden Menge von Wertekombinationen "dazuverzinst".

.. continue 

Das Informationmaß einer realen Variablen der Größe `C`, bei der Verwendung von Bits, 
ist die Anzahl `n=\log_2 C` von Bits, die notwendig sind, um die gleiche Vielzahl `C` zu erzeugen, damit wir au
Die reale Information ist aber die Größe der tatsächlichen Variablen.

.. note:: If we start from a *number of variables*, the *exponential function* gives the *number of value combinations*.
  If we start from a *number of values*, the *logarithm* gives the *number of variables* needed to represent it.

For **interest calculation** we look at an amount of money (the `1`), which is deposited in the bank with interest `i`.
After `n` years the `1` has grown to 

.. math::

    (1+i/100)^n = q^n
    
`q` is not `2`, normally just a little above `1`. 
The corresponding "information" measure in a financial context of interest `i` would be the number of years,
or whatever unit of *compounding* period one chooses to use.

The essential difference with respect to bit information is that what is added is a *fraction* of what is there.
But then, fraction is actually just a matter of units.

The units of living organisms are cells and the ultimate units in the real world are the quantum particles.
Both of them are small compared to the things around us. And with such small units one can also *compound* 
arbitrarily (infinitely) often:

.. math::

    \lim_{m->\infty}(1+\frac{x}{m})^m = \lim_{n->\infty}(1+\frac{1}{n})^{nx} = e^x

In the first equality we see that, given a certain growth, varying the *compounding steps*
amounts to varying the *growth rate*. 

.. note:: Actually in the financial world the real compounding takes place in very small steps, just that the bank
  forwards them to the customer in larger units of time for several reasons.

`x` is the information in the **natural information** unit `nat <https://en.wikipedia.org/wiki/Nat_(unit)>`_.
Basically we split up the size of the variable to infinitely many infinitely small fractional variables, 
whose size are just a very little bit larger than `1`.

