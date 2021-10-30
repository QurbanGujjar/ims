# import EAN13 from barcode module
from barcode import Gs1_128

# import ImageWriter to generate an image file
from barcode.writer import ImageWriter
number="0432"+"123456"
# Make sure to pass the number as string
# number = '5901234123457'

# Now, let's create an object of EAN13 class and
# pass the number with the ImageWriter() as the
# writer
my_code = Gs1_128(number, writer=ImageWriter())

# Our barcode is ready. Let's save it.
my_code.save("new_code3")
