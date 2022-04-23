import matplotlib.image as img
import matplotlib.pyplot as plt
import numpy as np

# Function for showing the image
def ShowImage(image,heading):
    plt.imshow(image)
    plt.title(heading)
    plt.show()


# Functino providing the Dimensions of the image
def ProvideDimension(image):
    return image.shape[0], image.shape[1]


# Function for defining the Lorenz Equations
def LorenzEquations(x, y, z):
    sigma = 10.0
    beta = 8.0/3.0
    rho = 28.0

    dx = (sigma*(y - x))
    dy = (rho*x - y - x*z)
    dz = (-1*(beta*z) + x*y)
    return dx, dy, dz


# Defining the Runge Kutte Method
def RungeKutte(x0, y0, z0, n):
   
    x = np.zeros(n+1)
    y = np.zeros(n+1)
    z = np.zeros(n+1)

    x[0] = x0
    y[0] = y0
    z[0] = z0

    T = 25
    dt = T/float(n)

    for k in range(n):
        k1, l1, m1 = LorenzEquations(x[k], y[k], z[k])
        k2, l2, m2 = LorenzEquations(x[k] + 0.5*k1*dt, y[k] + 0.5*l1*dt, z[k] + 0.5*m1*dt)
        k3, l3, m3 = LorenzEquations(x[k] + 0.5*k2*dt, y[k] + 0.5*l2*dt, z[k] + 0.5*m2*dt)
        k4, l4, m4 = LorenzEquations(x[k] + k3*dt, y[k] + l3*dt, z[k] + m3*dt)

        x[k+1] = x[k] + (dt*(k1 + 2*k2 + 2*k3 + k4) / 6)
        y[k+1] = y[k] + (dt*(l1 + 2*l2 + 2*l3 + l4) / 6)
        z[k+1] = z[k] + (dt*(m1 + 2*m2 + 2*m3 + m4) / 6)
    return z


# Taking the image as input
picture = img.imread('girl.jpg')
ShowImage(picture,"Actual Image")

# Taking the dimesions of the image using the function
h, w = ProvideDimension(picture)


# Using the key for each pixel of the image
keys = RungeKutte(0.08342, 0.0696969, 0.442056, h*w)

# Doing Encryption using the key and the given image
Encryption = np.zeros(shape=[h, w, 3], dtype=np.uint8)
Index = 0
for i in range(h):
    for j in range(w):
        keyIndex = (int((keys[Index]*pow(10, 5)) % 256))
        Encryption[i, j] = picture[i, j] ^ keyIndex
        Index += 1
ShowImage(Encryption,"Encrypted Image")


# Proper Decryption using actual key
Decryption = np.zeros(shape=[h, w, 3], dtype=np.uint8)
Index = 0
for i in range(h):
    for j in range(w):
        keyIndex = (int((keys[Index]*pow(10, 5)) % 256))
        Decryption[i, j] = Encryption[i, j] ^ keyIndex
        Index += 1
ShowImage(Decryption,'Decrypted Image with Actual key')


# Improper Decryption using different key
keys1 = RungeKutte(0.1, 0.2, 0.3, h*w)
Decryption = np.zeros(shape=[h, w, 3], dtype=np.uint8)
Index = 0
for i in range(h):
    for j in range(w):
        keyIndex = (int((keys1[Index]*pow(10, 5)) % 256))
        Decryption[i, j] = Encryption[i, j] ^ keyIndex
        Index += 1
ShowImage(Decryption,"Decrypted Image with incorrect key")
