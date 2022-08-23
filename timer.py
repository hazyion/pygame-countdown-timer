import pygame
import math
import time

def timestring(tiem):
	hours = str(int(int(tiem)/3600))
	minutes = int((int(tiem)%3600)/60)
	if minutes < 10:
		minutes = "0"+str(minutes)
	else:
		minutes = str(minutes)
	seconds = int(tiem)%60
	if seconds < 10:
		seconds = "0"+str(seconds)
	else:
		seconds = str(seconds)
	ms = round(math.modf(tiem)[0],2)
	if ms == 0.0 or int(ms*100)%10 == 0:
		ms = "0"+str(ms)[2:]
	else:
		ms = str(ms)[2:]
	
	return (hours, minutes, seconds, ms)

def update_blit(text, color, position, f):
	img = f.render(text, True, color)
	rect = img.get_rect()
	rect.topleft = position
	return (img, rect)

pygame.init()
running = True
display_screen = pygame.display.set_mode((500, 330))
pygame.display.set_caption("Countdown Timer")

font = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 20)

color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_lb = (84, 180, 196)
color_grey = (183, 183, 183)
left_button_top = 140
left_button_left = 170
right_button_top = 140
right_button_left = 270
button_height = 20
button_width = 60

left_button_rect = pygame.Rect(left_button_left, left_button_top, button_width, button_height)
left_button_border_rect = pygame.Rect(left_button_left+1, left_button_top+1, button_width-2, button_height-2)
right_button_rect = pygame.Rect(right_button_left, right_button_top, button_width, button_height)
right_button_border_rect = pygame.Rect(right_button_left+1, right_button_top+1, button_width-2, button_height-2)

t_pause = "pause"
offset_pause = 10
t_resume = "resume"
offset_resume = 6
t_reset = "reset"
offset_reset = 14
t_stop = "stop"
offset_stop = 16
offset_vertical = 3
left_text_pos = (left_button_left+offset_resume, left_button_top+offset_vertical)
right_text_pos = (right_button_left+offset_reset, right_button_top+offset_vertical)
left_text_img, left_text_rect = update_blit(t_resume, color_black, left_text_pos, font_small)
right_text_img, right_text_rect = update_blit(t_reset, color_black, right_text_pos, font_small)

text_start_pos = (120, 200)
text_start = "Press enter to Start"
text_start_color = (102, 204, 0)
img_start, rect_start = update_blit(text_start, text_start_color, text_start_pos, font)

init_time = 5.0
total_time = init_time
hours, minutes, seconds, ms = timestring(total_time)

timer = minutes+":"+seconds+":"+ms
timer_color = (216, 20, 40)
timer_pos = (183, 65)
img_st, rect_st = update_blit(timer, timer_color, timer_pos, font)

start, end = False, False
active_timer = False

gl_time = time.time()
prev_gl_time = time.time()
border_color = color_black
left_button_color, right_button_color = color_white, color_white
f_pause, f_reset, f_stop, f_resume = False, False, False, False
f_flash, f_sel = False, True
flash_time, prev_flash_time = time.time(), time.time()

t_sel = "Enter time in seconds: "
t_sel2 = "Press enter to continue"
sel_pos = (24, 130)
sel2_pos = (24, 160)
sel_img, sel_rect = update_blit(t_sel, color_white, sel_pos, font)
sel2_img, sel2_rect = update_blit(t_sel2, color_white, sel2_pos, font_small)

input = "0"
input_pos = (335, 130)
input_img, input_rect = update_blit(input, color_lb, input_pos, font)

t_legend = "H         M           S         MS"
legend_pos = (184, 94)
legend_img, legend_rect = update_blit(t_legend, color_white, legend_pos, pygame.font.SysFont(None, 16))

while running:
	display_screen.fill((1, 10, 21))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				if start:
					active_timer = True
					prev_gl_time = time.time()
					start = False
					f_resume = True

				if f_sel:
					total_time = int(input)
					hours, minutes, seconds, ms = timestring(total_time)
					timer = hours+":"+minutes+":"+seconds+":"+ms
					img_st, rect_st = update_blit(timer, timer_color, timer_pos, font)
					if total_time > 0.01:
						f_sel = False
						init_time = total_time
						start = True
			
			elif event.key == pygame.K_BACKSPACE:
				if len(input) > 2:
					input = input[:-1]
					input_img, input_rect = update_blit(input[1:], color_lb, input_pos, font)
				else:
					input = "0"
					input_img, input_rect = update_blit(input, color_lb, input_pos, font)
	
			else:
				try:
					int(event.unicode)
					if len(input) < 6:
						input += event.unicode
						input_img, input_rect = update_blit(input[1:], color_lb, input_pos, font)

				except ValueError:
					pass
			
		if event.type == pygame.MOUSEBUTTONDOWN:
			if left_button_rect.collidepoint(pygame.mouse.get_pos()) and not f_sel:
				if not start and not end:
					if active_timer:
						f_pause = True
					else:
						f_resume = True
			if right_button_rect.collidepoint(pygame.mouse.get_pos()) and not f_sel:
				if active_timer:
					f_stop = True
				else:
					f_reset = True

	if f_sel:
		display_screen.blit(sel_img, sel_rect)
		display_screen.blit(sel2_img, sel2_rect)
		display_screen.blit(input_img, input_rect)
		pygame.display.update()
		continue

	if active_timer:
		gl_time = time.time()
		total_time -= gl_time - prev_gl_time
		prev_gl_time = gl_time

		if total_time < 0.01:
			total_time = 0.00
			end = True
			f_stop = True
		
		hours, minutes, seconds, ms = timestring(total_time)
		timer = hours+":"+minutes+":"+seconds+":"+ms
		img_st, rect_st = update_blit(timer, timer_color, timer_pos, font)

	if f_resume:
		left_text_pos = list(left_text_pos)
		left_text_pos[0] += offset_pause - offset_resume
		left_text_pos = tuple(left_text_pos)
		right_text_pos = list(right_text_pos)
		right_text_pos[0] += offset_stop - offset_reset
		right_text_pos = tuple(right_text_pos)
		left_text_img, left_text_rect = update_blit(t_pause, color_black, left_text_pos, font_small)
		right_text_img, right_text_rect = update_blit(t_stop, color_black, right_text_pos, font_small)
		active_timer = True
		prev_gl_time = time.time()
		f_resume = False

	if f_stop or f_pause:
		left_text_pos = list(left_text_pos)
		left_text_pos[0] += offset_resume - offset_pause
		left_text_pos = tuple(left_text_pos)
		right_text_pos = list(right_text_pos)
		right_text_pos[0] += offset_reset - offset_stop
		right_text_pos = tuple(right_text_pos)
		left_text_img, left_text_rect = update_blit(t_resume, color_black, left_text_pos, font_small)
		right_text_img, right_text_rect = update_blit(t_reset, color_black, right_text_pos, font_small)
		active_timer = False
		if f_stop:
			f_stop = False

		if f_pause:
			f_pause = False

	if f_reset:
		total_time = init_time
		hours, minutes, seconds, ms = timestring(total_time)
		timer = hours+":"+minutes+":"+seconds+":"+ms
		img_st, rect_st = update_blit(timer, timer_color, timer_pos, font)
		f_reset = False
		start = True
		end = False

	if left_button_rect.collidepoint(pygame.mouse.get_pos()):
		left_button_color = color_grey
	else:
		left_button_color = color_white
	if right_button_rect.collidepoint(pygame.mouse.get_pos()):
		right_button_color = color_grey
	else:
		right_button_color = color_white

	display_screen.blit(img_st, rect_st)
	if not start:
		pygame.draw.rect(display_screen, left_button_color, left_button_rect)
		pygame.draw.rect(display_screen, border_color, left_button_border_rect, width = 1)
		pygame.draw.rect(display_screen, right_button_color, right_button_rect)
		pygame.draw.rect(display_screen, border_color, right_button_border_rect, width = 1)
		display_screen.blit(left_text_img, left_text_rect)
		display_screen.blit(right_text_img, right_text_rect)
	display_screen.blit(legend_img, legend_rect)
	
	if start:
		left_text_pos = (left_button_left+offset_resume, left_button_top+offset_vertical)
		right_text_pos = (right_button_left+offset_reset, right_button_top+offset_vertical)
		left_text_img, left_text_rect = update_blit(t_resume, color_black, left_text_pos, font_small)
		right_text_img, right_text_rect = update_blit(t_reset, color_black, right_text_pos, font_small)

		display_screen.blit(img_start, rect_start)

	if end:
		flash_time = time.time()
		if flash_time - prev_flash_time > 0.5:
			f_flash = not(f_flash)
			prev_flash_time = flash_time
		if f_flash:
			pygame.draw.circle(display_screen, (216, 20, 40), (150, 92), 10)
			pygame.draw.circle(display_screen, (216, 20, 40), (340, 92), 10)

	pygame.display.update()

pygame.quit()