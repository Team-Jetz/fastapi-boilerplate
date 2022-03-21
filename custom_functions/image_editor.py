from datetime import datetime
import random
import string

def img_file_name_generator(image):
    current_date = datetime.utcnow()
    epoch_time = current_date.timestamp()

    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}_{epoch_time}.'
    filename = new.join(image.filename.rsplit('.',1))
    # filename = new.join(epoch_time.rsplit('.',1))
    return filename