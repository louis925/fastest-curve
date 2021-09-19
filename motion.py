import numpy as np


class Motion:
  def __init__(self):
    pass

  def cal_acc(self, ball, curve):
    """Calculate acceleration"""
    raise NotImplementedError

  def cal_vel(self, ball, curve):
    """Calculate velocity"""
    raise NotImplementedError

  def cal_total_time_vel(self, ball, curve, steps=10000):
    """Calculate total time from integral"""
    raise NotImplementedError


class MotionSimple(Motion):
  """Simplest motion calculations

  Conditions:
    1. Frictionless
    2. Conservation of mechanical energy.
    3. The ball cannot detach from curve.
  """

  def __init__(self, params):
    super().__init__()

    self.g = params.g  # can be in base __init__() if dynamic g not needed

  def cal_vel(self, ball, curve):
    """Calculate velocity vector from the law of conservation of mechanical energy."""

    x, y = ball.x, ball.y
    m = curve.cal_slope(x)

    v = np.sqrt(2 * self.g * (curve.h - y))

    deno = np.sqrt(1 + m * m)
    vx = v / deno
    vy = v * m / deno

    return vx, vy

  def cal_acc(self, ball, curve):
    """Calculate acceleration vector from gravitational and constraint force."""

    x = ball.x
    vx = ball.vx
    m = curve.cal_slope(x)
    g = self.g
    curv = curve.cal_curvature(x)
    curv_term = curv * (vx * vx)
    deno = 1 + m * m
    ax = -(curv_term + g) * m / deno
    ay = (curv_term - g * m * m) / deno
    return ax, ay

  def cal_total_time_vel(self, ball, curve, steps=10000):
    dx = curve.w / steps
    x = np.arange(dx, curve.w + dx, dx)
    y = curve.cal_height(x)
    m = curve.cal_slope(x)

    return np.sum(np.sqrt((1 + m ** 2) / (2 * self.g * (curve.h - y)))) * dx
