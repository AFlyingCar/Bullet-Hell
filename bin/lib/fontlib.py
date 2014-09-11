#Tyler Robbins
#9/6/14
#Font Libraries
#Store functions to handle word-wrap and other font/word related things

from itertools import chain

#############################################################
# FUNCTIONS TO HANDLE WORD-WRAPPING							#
# THESE CAN BE FOUND HERE:									#
# http://www.pygame.org/wiki/TextWrapping?parent=CookBook	#
# THEY HAVE BEEN EDITED TO WORK BETTER WITH THE REST OF THE #
#  PROGRAM													#
#############################################################

def truncline(text,font,maxwidth):
	real=len(text)
	stext=text
	l=font.size(text)[0]
	cut=0
	a=0
	done=1
	old = None


	while l > maxwidth:
		a=a+1
		n=text.rsplit(None, a)[0]
		
		if stext == n:
			cut += 1
			stext= n[:-cut]
		
		else:
			stext = n
		
		l=font.size(stext)[0]
		real=len(stext)
		done=0  

	return real, done, stext

def wrapline(text,font,surf,textpos): 
	maxwidth = surf.get_width()-textpos[0]

	done=0
	wrapped=[]

	while not done:
		nl, done, stext=truncline(text, font, maxwidth)
		wrapped.append(stext.strip())
		text=text[nl:] 

	return wrapped

def wrap_multi_line(text, font, maxwidth):
	""" returns text taking new lines into account.
	"""
	lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
	return list(lines)

nuclear = u'\u2622'