# SNIPPET: animated steps for any event. The pattern stays the .webp still; show_video
# derives the Movie image name: "anim_" + webp basename with spaces -> underscores.
#
# Pattern on the event:
#     Pattern("main", "images/events/gym/my_clip/my_clip <school_level> <step>.webp")
#
# One Movie per <school_level> x <step> that has a clip. Always ship the start_image.

define anim_my_clip_path = "images/events/gym/my_clip/my_clip "
image anim_my_clip_2_0 = Movie(play = anim_my_clip_path + "2 0.webm", start_image = anim_my_clip_path + "2 0.webp", loop = True)
image anim_my_clip_2_1 = Movie(play = anim_my_clip_path + "2 1.webm", start_image = anim_my_clip_path + "2 1.webp", loop = True)

# In the label (mix freely with image.show for stills):
#     $ image = convert_pattern("main", **kwargs)
#     $ image.show_video(0, True)     # play step 0, wait for a click
#     $ image.show_video(1, True)
#     $ image.show(2)                 # a still
