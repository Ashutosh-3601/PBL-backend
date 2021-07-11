from Providers import MongoProvider
from Services import CompareService
from Services import CameraService
from Providers import ColorProvider 
import dotenv
import os

dotenv.load_dotenv()
CLR = ColorProvider.Colors

print(f"{CLR.CBOLD}{CLR.CVIOLETBG2}Starting up the ATM{CLR.CEND}")
try:
    MongoService = MongoProvider.MongoStore(os.environ.get('URL'))
    MongoService.connect()
except RuntimeError as error:
    print(error)
    exit(0)

print(f"\n{CLR.CURL}{CLR.CGREEN}Welcome to ATM{CLR.CEND}\n")
# Review 1 input
cardNumber = input(f"{CLR.CBLUE}{CLR.CBOLD}Enter the card number:\n{CLR.CEND}")

if len(cardNumber) != 9:
    print(f"{CLR.CRED}Invalid card number!{CLR.CEND}")
    exit(0)

facesLinkedWithCard = MongoService.get('faces', {'no': f'{cardNumber}'})

if facesLinkedWithCard is None:
    print(f'{CLR.CRED}[Error] Cannot find card accociated with card number!{CLR.CEND}')
    exit(0)

userFace = CameraService.CameraService(cardNumber, 10)
captured = userFace.capture()
if not captured:
    print(f'{CLR.CRED2}Error capturing your image!{CLR.CEND}')
    exit(0)

comparedList = []
print(f'{CLR.CYELLOW}[Internal] Started Comparing Faces{CLR.CEND}')
for img in facesLinkedWithCard['image']:
    location = img['location']
    try:
        comp = CompareService.CompareImg()
        faceCompare = comp.compare(location, f'image/{cardNumber}.jpg')
    except RuntimeError as error:
        print(f'{CLR.CRED}error{CLR.CEND}')
    else: 
        if faceCompare < 0.4:
            comparedList.append({'name': img['name'], 'distance': faceCompare})

# delete
def delCaptured():
    os.remove(f'image/{cardNumber}.jpg')
    print(f'{CLR.CGREEN2} Cleared the captured image{CLR.CEND}')

if len(comparedList) == 0:
    print(f'{CLR.CRED}[Internal] Face didn\'t match with face(s) in card!{CLR.CEND}')
    delCaptured()
    exit(0)

bestMatch = comparedList[0]
print(f'{CLR.CYELLOW}[Internal] Getting best matched face{CLR.CEND}')
if len(comparedList) > 1:
    for index in range(1, len(comparedList)):
        curItem = comparedList[index]
        if curItem['distance'] < bestMatch['distance']:
            bestMatch = curItem

result = '{}[Internal] {}Best matched face: {} with difference in face for value {}{}'
print(result.format(CLR.CBEIGE2, CLR.CURL, bestMatch['name'], round(bestMatch['distance'][0],2), CLR.CEND))

delCaptured()
print(f'\n{CLR.CREDBG}Enter your pin:{CLR.CEND}')