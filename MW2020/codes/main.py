import pygame
import time
import numpy as np

from matplotlib import pyplot as plt

########################################################################################################################
# ### class representing the lander module
########################################################################################################################

MY_PI = 3.14

GRAV_ACC_MOON = 1.62

MY_EPS = 1e-7

class LunarLander:
	
	mass = 16400.0			# we assume constant mass
	vrtlThrst = 45000.0
	hrzntlThrst = 500.0
	
	height = 90
	width = 90

	# initial position
	posX_0 = 20.0
	posY_0 = 40.0

	# initial linear velocity
	velX_0 = 0.0
	velY_0 = 0.0

	# initial heading
	alpha_0 = MY_PI / 2

	# initial angular velocity
	omega_0 = 0.0

	def __init__(self): 

		# fix image which represents the lunar lander
		self.image = pygame.transform.smoothscale(pygame.image.load('./images/lander.png'), (self.width, self.height))
				# self.image = pygame.transform.smoothscale(pygame.image.load('images\lander.png'), (self.width, self.height))		# Windows

		# get rectancle which encloses the image
		self.rect = self.image.get_rect()

		# initialse x, y position of lander 
		# RECALL:
		#	the axis in pygame are given as follows:
		#
		#			----------> x
		#			|
		#			|
		#			|
		#			|
		#			y
		# 
		self.posX = 0
		self.posY = 0
		self.setPos(self.posX_0, self.posY_0)
		
		# initialise heading of the lander
		self.alpha = 0
		self.setHeading(self.alpha_0)
		
		# initialise velocities in x, y direction and angle velocity of the lander
		self.velX = 0
		self.velY = 0
		self.setLinVel(self.velX_0, self.velY_0)

		# initialise angular velocity
		self.omega = 0
		self.setAngVel(self.omega_0)

	# ### update function

	def update(self, acc_x, acc_y, acc_w, dt):

		pos = self.getPos()
		vel = self.getLinVel()
		omega = self.getAngVel()

		vel[0] += acc_x * dt
		vel[1] += acc_y * dt
		omega += acc_w * dt
		
		pos[0] += vel[0] * dt
		pos[1] -= vel[1] * dt

		self.setPos(pos[0], pos[1])
		self.setLinVel(vel[0], vel[1])
		self.setAngVel(omega)

	# ### getter 

	def getPos(self):
		return np.array([self.posX, self.posY])

	def getHeading(self):
		return self.alpha

	def getLinVel(self):
		return np.array([self.velX, self.velY])

	def getAngVel(self):
		return self.omega
		
	def getVrtlThrst(self):
		return self.vrtlThrst

	def getHrzntlThrst(self):
		return self.hrzntlThrst

	def getMass(self):
		return self.mass

	# ### setter 

	def setPos(self, x, y):
		self.posX = x
		self.posY = y

	def setHeading(self, alpha):
		self.alpha = alpha

	def setLinVel(self, v_x, v_y):
		self.velX = v_x
		self.velY = v_y

	def setAngVel(self, omega):
		self.omega = omega

########################################################################################################################
# ### controller functions
########################################################################################################################

def humanController(pressed):

	u1 = 0
	u2 = 0
	
	if pressed[pygame.K_UP]:
		u1 = 1
	
	if pressed[pygame.K_RIGHT]:
		u2 = 1
	elif pressed[pygame.K_LEFT]:
		u2 = -1
		
	return u1, u2

def myPIDFunc(prevErr, currErr, prevIntGain, kp, ki, kd, dt):
	"""
		@param[in] ### err ### error term
		@param[in] ### i0 ### previous integral gain
		@param[in] ### kp ### constant for p-gain
		@param[in] ### ki ### constant for i-gain
		@param[in] ### kd ###constant for d-gain

		@return ### retVal ### numpy array containing the p, i, and d value
	"""

	p = kp * currErr
	i = prevIntGain + dt * ki * currErr
	d = kd * (1.0 / dt) * (currErr - prevErr)

	retVal = np.array([p, i, d])

	return retVal

########################################################################################################################
# ### class representing the controller
########################################################################################################################

class MyControllerClass:

	# parameter values for pid control
	kp_x = 3.0
	kp_y = 9.5

	ki_x = 0.0
	ki_y = 0.05

	kd_x = 109.0
	kd_y = 59.9

	def __init__(self, targetPos):
		self.trgtPos = targetPos

		self.interPos = np.array([targetPos[0], targetPos[1] * 0.5])

		# integral gain values needed for the pid part of the controller
		self.i_x = 0.0
		self.i_y = 0.0

		self.reachedLandingZone = False

		self.yVelDiff = -0.0005

	def getControlValues(self, currPos, prevPos, currLinVel, currMass, vrtlThrst, dt):

		u_x = 0.0
		u_y = 0.0

		self.reachedLandingZone = self.reachedLandingZone or \
			((np.linalg.norm(currPos - self.interPos, 2) <= 15) and (np.linalg.norm(currLinVel, 2) <= 0.1))
		
		targetApprReached = np.abs(currPos[1] - self.trgtPos[1]) < 0.25

		if not targetApprReached:
			if not self.reachedLandingZone:
				# phase 1: pid control to reach intermediate position
				b_y = 0.0
				currErr_y = -(self.interPos[1] - currPos[1]) / (currPos[1] + MY_EPS)
				prevErr_y = -(self.interPos[1] - prevPos[1]) / (prevPos[1] + MY_EPS)
				p_y, i_y, d_y = myPIDFunc(prevErr_y, currErr_y, self.i_y, self.kp_y, self.ki_y, self.kd_y, dt)

				u_y = np.clip(1 + b_y + np.clip(p_y + i_y + d_y, -1, 1), 0, 1)
			else:
				# phase 2: landing phase
				u_y = (self.yVelDiff / dt + GRAV_ACC_MOON) / (vrtlThrst / currMass)


			# control for horizontal thrust
			currErr_x = (self.interPos[0] - currPos[0]) / (currPos[0] + MY_EPS)
			prevErr_x = (self.interPos[0] - prevPos[0]) / (prevPos[0] + MY_EPS)
			p_x, i_x, d_x = myPIDFunc(prevErr_x, currErr_x, self.i_x, self.kp_x, self.ki_x, self.kd_x, dt)

			u_x = np.clip(p_x + i_x + d_x, -1, 1)

		return u_x, u_y, targetApprReached



########################################################################################################################
# ### class representing the simulation
########################################################################################################################

class Game:
	
	dt = 0.1
	
	trgtPos = np.array([300, 480])

	bndWidth = 20
	scrWidth = 841
	scrHeight = 595
	
	white = (255, 255, 255)

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((self.scrWidth + 2 * self.bndWidth, self.scrHeight + 2 * self.bndWidth))

		self.bckgrndImg = pygame.transform.smoothscale(pygame.image.load('./images/background.png'), (self.scrWidth, self.scrHeight))		# Linux
				# self.bckgrndImg = pygame.image.load('images\background.png')		# Windows
				
		self.initBoundary()
		self.initLander()

		self.controller = MyControllerClass(self.trgtPos)

	def initBoundary(self):
		self.bndryLeft = pygame.Rect(0, self.bndWidth, self.bndWidth, self.scrHeight)
		self.bndryRight = pygame.Rect(self.scrWidth + self.bndWidth, self.bndWidth, self.bndWidth, self.scrHeight)
		self.bndryTop = pygame.Rect(0, 0, self.scrWidth + 2 * self.bndWidth, self.bndWidth)
		self.bndryBottom = pygame.Rect(0, self.scrHeight + self.bndWidth, self.scrWidth + 2 * self.bndWidth, self.bndWidth)
		
	def initLander(self):
		self.lander = LunarLander()

	def collisionDetection(self):
		return self.lander.rect.colliderect(self.bndryLeft) or self.lander.rect.colliderect(self.bndryRight) \
			or self.lander.rect.colliderect(self.bndryTop) or self.lander.rect.colliderect(self.bndryBottom)

	def update(self, u_x, u_y):

		m = self.lander.getMass()

		f1 = u_y * self.lander.getVrtlThrst()
		f2 = u_x * self.lander.getHrzntlThrst()
		f3 = m * GRAV_ACC_MOON

		alpha = self.lander.getHeading()
		c = np.cos(alpha)
		s = np.sin(alpha)

		hrzntlFrc = f2 * s + f1 * c
		vrtlFrc = f1 * s - f2 * c

		acc_x = (1 / m) * hrzntlFrc
		acc_y = (1 / m) * (-f3 + vrtlFrc)
		
		# omit for the sake of simplicity the impact of steering maneuvers on the angular velocity
		# of the landing module
		acc_w = 0			

		self.lander.update(acc_x, acc_y, acc_w, self.dt)

	def render(self):
		# draw boundaries of the screen - which act as boundaries of the screen. if lander touches on of those, then
		# game is over!
		pygame.draw.rect(self.screen, self.white, self.bndryLeft)
		pygame.draw.rect(self.screen, self.white, self.bndryRight)
		pygame.draw.rect(self.screen, self.white, self.bndryTop)
		pygame.draw.rect(self.screen, self.white, self.bndryBottom)
		
		# draw background image
		self.screen.blit(self.bckgrndImg, (self.bndWidth, self.bndWidth))
		
		# draw lander
		self.screen.blit(self.lander.image, (self.lander.posX, self.lander.posY))
		self.lander.rect = pygame.Rect(self.lander.posX, self.lander.posY, self.lander.width, self.lander.height)
		pygame.display.flip()
	
	def renderFinalScreen(self):
		pass

	def run(self):

		xPosList = []
		yPosList = []		

		xVelList = []
		yVelList = []

		currPos = self.lander.getPos()
		prevPos = self.lander.getPos()

		maxTimeSteps = 10000
		t = 0
		done = False
		exit = False
		while (not exit) and (t < maxTimeSteps):
			if pygame.event.get(pygame.QUIT):
				exit = True

			t += 1

			xPosList.append(currPos[0])
			yPosList.append(currPos[1])
		
			currLinVel = self.lander.getLinVel()
			xVelList.append(currLinVel[0])
			yVelList.append(currLinVel[1])

			###############################################################
			#
			# HERE CONTROLLER HAS TO BE CHOSEN
			#
			###############################################################
		
			# ---- human controller
			# pressed = pygame.key.get_pressed()
			# u1, u2 = humanController(pressed)
			
			# ---- pid control
			currPos = self.lander.getPos()

			u_x, u_y, done = self.controller.getControlValues(currPos, prevPos, currLinVel,\
				self.lander.getMass(), self.lander.getVrtlThrst(), self.dt)

			prevPos = currPos.copy()

			# update
			self.update(u_x, u_y)
			
			# method which draws every object ...
			self.render()
	
			exit = self.collisionDetection() or done
			
		
		self.renderFinalScreen()
		pygame.quit()

		if done:
			print('>>> mission succeeded.')

		n_x = len(xPosList)
		n_y = len(yPosList)

		fig1 = plt.figure()

		ax1 = fig1.add_subplot(2, 2, 1)
		ax1.plot(np.arange(0, n_x), xPosList)
		ax1.plot(np.arange(0, n_x), np.ones(n_x) * self.trgtPos[0], linestyle = '--', color = 'r')
		ax1.set_xlabel('t')
		ax1.set_ylabel('x')
		ax1.set_title('x position vs. time')

		ax2 = fig1.add_subplot(2, 2, 2)
		ax2.plot(np.arange(0, n_y), yPosList)
		ax2.plot(np.arange(0, n_y), np.ones(n_y) * self.trgtPos[1], linestyle = '--', color = 'r')
		ax2.plot(np.arange(0, n_y), np.ones(n_y) * self.trgtPos[1] * 0.5, linestyle = '--', color = 'orange')
		ax2.set_xlabel('t')
		ax2.set_ylabel('y')
		ax2.set_title('y position vs. time')

		ax3 = fig1.add_subplot(2, 2, 3)
		ax3.plot(np.arange(0, n_y), xVelList)
		ax3.set_xlabel('t')
		ax3.set_ylabel('v_x')
		ax3.set_title('x linear velocity vs. time')

		ax4 = fig1.add_subplot(2, 2, 4)
		ax4.plot(np.arange(0, n_y), yVelList)
		ax4.set_xlabel('t')
		ax4.set_ylabel('v_y')
		ax4.set_title('y linear velocity vs. time')

		# fit plot to full screen
		# figMngr = plt.get_current_fig_manager()
		# figMngr.full_screen_toggle()

		# fig2 = plt.figure()
		# ax = fig2.add_subplot(1, 1, 1)
		# ax.plot(xPosList, yPosList)
		# ax.set_xlabel('x')
		# ax.set_ylabel('y')
		# ax.set_title('phase plot')

		plt.show()

if __name__ == '__main__':
	
	game = Game()
	game.run()

