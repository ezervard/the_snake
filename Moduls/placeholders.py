import pygame.font

pygame.init()

RED_CLR = (130, 39, 27)

pause_text = pygame.font.SysFont('Arial', 32).render('Pause', True, pygame.color.Color('White'))
pause_info = pygame.font.SysFont('Arial', 24).render('press SPACE to continue', True, pygame.color.Color('White'))

loose_text = pygame.font.SysFont('Arial', 32).render('Game over', True, pygame.color.Color(RED_CLR))
loose_info = pygame.font.SysFont('Arial', 24).render('Press SPACE to restart', True, pygame.color.Color(RED_CLR))
loose_font = pygame.font.Font(None, 35)
loose_score = pygame.font.SysFont('Arial', 28).render('', True, pygame.color.Color(RED_CLR))


score_font = pygame.font.Font(None, 24)
score_text = score_font.render("Score: 0", True, pygame.color.Color("White"))


state_text = pygame.font.SysFont('comic sans', 50).render('AI PLAYED', True, pygame.color.Color(RED_CLR))

info_font = pygame.font.Font(None, 24)
info = info_font.render('Press SPACE to Pause  or  ESC to Close', True, pygame.color.Color(50, 50, 50))