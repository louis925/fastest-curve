class Ball:
  def __init__(self, x, y, vx=0, vy=0):
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy

  def _update_from_acc(self, curve, motion, dt):
    # TODO: consider using Verlet or other update algos

    ax, ay = motion.cal_acc(self, curve)
    self.vx += 0.5 * ax * dt
    self.vy += 0.5 * ay * dt
    self.x += self.vx * dt
    self.y += self.vy * dt
    self.vx += 0.5 * ax * dt
    self.vy += 0.5 * ay * dt

    curve_height_x = curve.cal_height(self.x)
    if self.y < curve_height_x:
      self.y = curve_height_x  # ball not penatrate into curve

  def _update_from_vel(self, curve, motion, dt):
    self.x += self.vx * dt
    self.y += self.vy * dt
    
    curve_height_x = curve.cal_height(self.x)
    if self.y < curve_height_x:
      self.y = curve_height_x  # ball not penatrate into curve
    
    self.vx, self.vy = motion.cal_vel(self, curve)

  def update(self, curve, motion, dt, type='vel'):
    if type == 'acc':
      self._update_from_acc(curve, motion, dt)
    elif type == 'vel':
      self._update_from_vel(curve, motion, dt)
    else:
      raise ValueError(f'wrong update type: {type}')

  def check_vxLT0(self):
    return self.vx < 0

  def check_goal(self, W):
    return self.x >= W