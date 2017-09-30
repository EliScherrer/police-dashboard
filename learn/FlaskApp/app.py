from flask import Flask, render_template, json, request, make_response
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/test.png')
def simple():
    import datetime
    import StringIO
    import random

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    lista = ['2005', '09/2002', 'A freaking awesome time', 'lorem']
    a = json.dumps(lista)
    listb = ['06/2002', '09/2003', 'Some great memories', 'ipsum']
    listc = ['2003', 'Had very bad luck']

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return render_template(
        'index.html',**locals())


if __name__ == "__main__":
    app.run(debug = True)
