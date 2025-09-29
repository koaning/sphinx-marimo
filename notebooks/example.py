import marimo

__generated_with = "0.1.0"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __(mo):
    mo.md("# Welcome to Marimo!")
    return


@app.cell
def __(mo):
    slider = mo.ui.slider(1, 10, value=5, label="Select a value")
    slider
    return slider,


@app.cell
def __(mo, slider):
    mo.md(f"You selected: **{slider.value}**")
    return


@app.cell
def __():
    import matplotlib.pyplot as plt
    import numpy as np
    return np, plt


@app.cell
def __(np, plt, slider):
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(slider.value * x)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, y)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(f"Sin({slider.value}x)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig
    return ax, fig, x, y


@app.cell
def __(mo):
    mo.md("""
    ## Interactive Features

    This notebook demonstrates:
    - Reactive UI components
    - Real-time updates
    - Matplotlib integration
    - Markdown rendering

    Try adjusting the slider above to see the plot update!
    """)
    return


if __name__ == "__main__":
    app.run()