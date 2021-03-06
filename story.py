import os
import json
import requests
from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps

import settings
from test_named_tuple import create_song_story_data, create_artist_story_data

class Story:
	def __init__(self):
		self.W = 1080
		self.H = 1920

	def create_header(self, draw):
		font = ImageFont.truetype(settings.HEADER_FONT, settings.HEADER_FONT_SIZE)
		text_width, text_height = font.getsize(settings.HEADER_TEXT)
		draw.text(((self.W-text_width)/2, settings.HEADER_POSITION_HEIGHT), settings.HEADER_TEXT, font=font, fill=settings.HEADER_FONT_COLOR)

	def create_footer(self, draw):
		font = ImageFont. truetype(settings.FOOTER_FONT, settings.FOOTER_FONT_SIZE)
		draw.text((settings.FOOTER_POSITION), settings.FOOTER_TEXT, font=font, fill=settings.FOOTER_FONT_COLOR)

	def create_mask(self, x, y):
		bigsize = (x * 3, y * 3)
		mask = Image.new('L', bigsize, 0)
		draw = ImageDraw.Draw(mask) 
		draw.ellipse((0, 0) + bigsize, fill=255)
		mask = mask.resize((x, y), Image.ANTIALIAS)
		return mask

class SongStory(Story):

	def __init__(self, artists, songs, images):
		super(SongStory, self).__init__()
		self.songs = songs
		self.artists = artists
		self.images = images

	def create_image(self):
		base = Image.new('RGB', (self.W, self.H), ImageColor.getrgb(settings.BASE_COLOR))
		draw = ImageDraw.Draw(base)

		self.header = self.create_header(draw)
		self.footer = self.create_footer(draw)
		# todo
		self.mask = self.create_mask(128, 130)
		self.thumbnails = self.create_song_thumbnails(self.mask, base)
		self.text = self.create_song_and_artist_text(draw)
		# base.show()
		base.save("song_story_test.jpg")

	def create_song_thumbnails(self, mask, base):
		# todo, fix i
		i = 0
		for filename in self.images:
			if filename.endswith(".jpg"):
				img = Image.open(filename)
				#todo
				new_img = img.resize((128,130))
				new_img.putalpha(mask)
				base.paste(new_img, settings.SONG_THUMBNAIL_POSITION[i], mask)
				i+=1

	def create_song_and_artist_text(self, draw):

		song_font = ImageFont.truetype(settings.SONG_TEXT_FONT, settings.SONG_TEXT_SIZE)
		artist_font = ImageFont.truetype(settings.ARTIST_TEXT_FONT , settings.ARTIST_TEXT_SIZE)

		for i in range(10):
			draw.text(settings.SONG_TEXT_POSITION[i], self.songs[i], font=song_font, fill=settings.SONG_STORY_FONT_COLOR)
			draw.text(settings.ARTIST_TEXT_POSITION[i], self.artists[i], font=artist_font, fill=settings.SONG_STORY_FONT_COLOR)


class ArtistStory(Story):

	def __init__(self, artists, images):
		super(ArtistStory, self).__init__()
		self.artists = artists
		self.images = images

	def create_image(self):
		base = Image.new('RGB', (self.W, self.H), ImageColor.getrgb(settings.BASE_COLOR))
		draw = ImageDraw.Draw(base)

		self.header = self.create_header(draw)
		self.footer = self.create_footer(draw)
		self.mask = self.create_mask(250, 250)
		self.thumbnails = self.create_thumbnails(self.mask, base)
		# base.show()
		base.save("artist_story_test.jpg")

	def create_thumbnails(self, mask, base):

		i = 0
		for filename in self.images:
			if filename.endswith(".jpg"):
				img = Image.open(filename)
				new_img = img.resize((250,250))

				new_img.putalpha(mask)
				base.paste(new_img, settings.ARTIST_PHOTO_POSITION[i], mask)
				i+=1


response = create_artist_story_data()
a = ArtistStory(response.artists, response.images)
# print(a.__dict__)
# print(a.create_image())

response = create_song_story_data()
s = SongStory(response.artists, response.songs, response.images)
# print(s.__dict__)
# print(s.create_image())






