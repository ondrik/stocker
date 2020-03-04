# Contains auxiliary plotting functions

import bokeh.plotting as bkplt
import bokeh.embed as bkem

###########################################
def plot_candlestick(df, width, height):
    """plot_candlestick(df) -> (plot_script, plot_img)

Plots a Pandas's data frame with time data into a candlestick bar.
The data frame is assumed to have (at least) the following columns:
"time", "open", "close", "high", "low", "volume".

The function returns a pair consisting of a JavaScript script and an image.
"""
    plot = bkplt.figure(
            x_axis_type='datetime',
            plot_width=width,
            plot_height=height)

    inc = df.close > df.open
    dec = df.open > df.close
    # TODO: needs to be changed
    w = 12*60*60*1000 # half day in ms

    # plot the candles
    plot.segment(df.time, df.high, df.time, df.low, color="black")
    plot.vbar(df.time[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    plot.vbar(df.time[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")

    return bkem.components(plot)
