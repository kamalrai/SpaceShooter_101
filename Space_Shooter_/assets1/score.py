def show_score(x, y):
    score = font.render("Score : " + str(score_value) + " Highscore" + str(highscore), True, (255, 255, 255))
    screen.blit(score, (x, y))
