import prometheus_client

from flask import Flask, request
from werkzeug.middleware.dispatcher import DispatcherMiddleware

METRICS_REGISTRY = prometheus_client.CollectorRegistry()

TRAIN_VALIDATION = 'train_validation'

METRICS = {
    TRAIN_VALIDATION: prometheus_client.Gauge(
        TRAIN_VALIDATION,
        documentation=f'explains the drift in metrics for model from validation routine',
        labelnames=['model', 'metric'],
        registry=METRICS_REGISTRY
    )
}

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': prometheus_client.make_wsgi_app(registry=METRICS_REGISTRY)
})


@app.route(f'/{TRAIN_VALIDATION}', methods = ['POST'])
def update_model_metric():
    model = request.args.get('model', type=str)
    metric = request.args.get('metric', type=str)
    value = request.args.get('value', type=float)

    METRICS[TRAIN_VALIDATION].labels(model=model, metric=metric).set(value)

    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5445, debug=False)