import numpy as np
import matplotlib.pyplot as plt


class Curve:
  def __init__(self):
    pass

  def cal_height(self, x):
    raise NotImplementedError

  def cal_slope(self, x):
    raise NotImplementedError

  def cal_curvature(self, x):
    raise NotImplementedError

  def generate(self):
    raise NotImplementedError

  def check_valid_curve(self):
      # TODO (louis): add tolerance
    if np.abs(self.cal_height(x=0) - self.h) > 1e-2:
      return False
    if np.abs(self.cal_height(x=self.w) - 0) > 1e-2:
      return False
    return True

  def plot(self, show=False, **kwargs):
    x = np.linspace(0, self.w, 100)
    y = self.cal_height(x)
    plt.plot(x, y, **kwargs)
    plt.xlabel('x')
    plt.ylabel('y(x)')
    if show:
      plt.show()


class CurveLinear(Curve):
  """curve: y = A * x + B, where A=-h/w, B=h."""

  def __init__(self, h, w):
    super().__init__()
    self.A = - h / w
    self.B = h
    self.h = h
    self.w = w

  @staticmethod
  def curve(A, B, x):
    return A * x + B

  def cal_height(self, x):
    return self.curve(self.A, self.B, x)

  def cal_slope(self, x):
    return self.A

  def cal_curvature(self, x):
    return 0.

  @classmethod
  def generate(cls, h, w):
    return cls(h, w)


class CurveExp(Curve):
  """curve: y = A * exp(-Bx) + C."""

  def __init__(self, A, B, C, h, w):
    super().__init__()
    self.A = A
    self.B = B
    self.C = C
    self.h = h
    self.w = w

  @staticmethod
  def curve(A, B, C, x):
    return A * np.exp(-B * x) + C

  def cal_height(self, x):
    return self.curve(self.A, self.B, self.C, x)

  def cal_slope(self, x):
    return - self.A * self.B * np.exp(-self.B * x)

  def cal_curvature(self, x):
    return self.A * self.B * self.B * np.exp(-self.B * x)

  @staticmethod
  def _cal_A_C(B, h, w):
    """
    For fixed B, h, and w, A and C are uniquely determined by the boundary
    condition y(0) = h and y(w) = 0, which give
        A = h / (1 - exp(-Bw)); C = - h / (exp(Bw) - 1).
    """
    A = h / (1 - np.exp(-B * w))
    C = -h / (np.exp(B * w) - 1)
    return A, C

  @classmethod
  def generate_from_B(cls, B, h, w):
    A, C = cls._cal_A_C(B, h, w)
    return cls(A, B, C, h, w)

  @classmethod
  def generate(cls, h, w, B_range=(0.01, 100)):
    """Random generate a viable exponential curve."""
    # generate B
    # NOTE: B can only be positive.
    B = np.random.uniform(*B_range) / w

    # generate instance
    return cls.generate_from_B(B, h, w)


class CurveParabola(Curve):
  """curve: y = A x^2 + B x + C."""

  def __init__(self, A, B, C, h, w):
    super().__init__()
    self.A = A
    self.B = B
    self.C = C
    self.h = h
    self.w = w

  @staticmethod
  def curve(A, B, C, x):
    return A * x * x + B * x + C

  def cal_height(self, x):
    return self.curve(self.A, self.B, self.C, x)

  def cal_slope(self, x):
    return 2 * self.A * x + self.B

  def cal_curvature(self, x):
    return 2 * self.A

  @staticmethod
  def _cal_B_C(A, h, w):
    """
    For fixed A, h, and w, B and C are uniquely determined by the boundary
    condition y(0) = h and y(w) = 0, which give
        A = h / (1 - exp(-Bw)); C = h.
    """
    B = -A * w - h / w
    C = h
    return B, C

  @classmethod
  def generate_from_A(cls, A, h, w):
    B, C = cls._cal_B_C(A, h, w)
    return cls(A, B, C, h, w)

  @classmethod
  def generate(cls, h, w, A_range=(0, 10)):
    """Random generate a viable exponential curve."""
    # generate A
    # NOTE: A can only be positive.
    A = np.random.uniform(*A_range) / w

    # generate instance
    return cls.generate_from_A(A, h, w)
