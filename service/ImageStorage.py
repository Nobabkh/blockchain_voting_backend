import base64
from PIL import Image
import io
import imghdr
import mimetypes  # Import the mimetypes module
from database.databaseConfig.databaseConfig import SessionLocal
from dto.OnlyUrlDTO import OnlyUrlDTO
from dto.UserDTO import UserDTO
from dto.ImageDTO import ImageDTO
from database.entity.KYC import KYC

BASEPATH = "/var/www/assets.genwebbuilder.com/"
BASEPATHDEV = '/var/projects/sparkweb_backend_v2/userimage'

def save_image_from_data_uri(data_uri, file_path) -> bool:
    # Remove the data URI prefix
    image_data = data_uri.split(',')[1]
    try:
        # Decode the base64 image data
        image_bytes = base64.b64decode(image_data)
        
        extension = data_uri.split(';')[0].split('/')[-1]
        if extension == 'svg+xml':
            extension = 'svg'
        
        # Open the image using PIL
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert the image to RGB mode if it's in RGBA mode
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        file_path = file_path + '.' + extension
        
        # Save the image to the specified file path with appropriate extension
        image.save(file_path)
        return True, '.' + extension
    except Exception as e:
        print(e)
        return False, '.png'

    
def savephoto(user: UserDTO, image: ImageDTO) -> OnlyUrlDTO:
    session = SessionLocal()
    userimgnum = session.query(KYC).filter_by(user_id=user.id).count()
    imgnum = 0
    if userimgnum != None:
        imgnum = userimgnum
    imagepath = BASEPATHDEV+user.email+str(imgnum)
    url = user.email+str(imgnum)
    try:
        saved, extain = save_image_from_data_uri(image.img[0], imagepath)
        if saved:
            print("image saved done")
            session.add(KYC(image=BASEPATHDEV+url+extain, user_id=user.id))
            print("image saved in db")
            session.commit()
            session.flush()
            session.close()
            print(url+extain)
            return OnlyUrlDTO(url=BASEPATHDEV+url+extain)
        else:
            return OnlyUrlDTO(url='None')
    except Exception as e:
        return OnlyUrlDTO('None')
    
import base64

def get_image_base64(image_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(image_path)
    
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Create the Base64 data URL with the MIME type prefix
    base64_string_with_prefix = f"data:{mime_type};base64,{encoded_string}"
    return base64_string_with_prefix

        
    
    
    