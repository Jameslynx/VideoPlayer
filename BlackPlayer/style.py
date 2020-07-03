stylesheet = """
QSlider#positionSlider::groove:horizontal {
    background: rgba(255, 255, 255, 100);
    height: 20px;
}

QSlider#positionSlider::sub-page:horizontal {
    background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
        stop: 0 #830, stop: 1 #F27);
    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
        stop: 0 #F27, stop: 1 #F2E);
    height: 20px;
}

QSlider#positionSlider::add-page:horizontal {
    background: rgba(255, 255, 255, 100);
    height: 20px;
}

QSlider#positionSlider::handle:horizontal {
    background: #F2E;
    border: 0px;
    width: 0x;
    margin-top: 0px;
    margin-bottom: 0px;
    border-radius: 0px;
}
"""
