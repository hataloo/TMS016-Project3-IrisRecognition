from calculateIris import *
from findIris import find_iris_adjusted
from irisNormalization import normalizeNonconcentric

from loadData import getDatasetImagePaths


def computeNormalizedIrisAndSave(path, closeFigAfter = True, saveResults = True):
    exampleImage = Image.open(path)
    exampleArray = np.array(exampleImage)


    gray_image = preprocess_image(exampleArray)

    outer_boundary = find_iris_adjusted(gray_image, daugman_start=35, daugman_end=80, daugman_step=1, points_step=2)
    iris_center, iris_rad = outer_boundary

    pupil_crop = preprocess_pupil(gray_image, iris_center, iris_rad)
    inner_boundary = find_iris_adjusted(pupil_crop, daugman_start=round(0.3*iris_rad), daugman_end=round(0.8*iris_rad), daugman_step=1, points_step=2)
    pupil_center, pupil_rad = inner_boundary

    normalized = normalizeNonconcentric(gray_image, iris_center, iris_rad, pupil_center, pupil_rad)
    enhanced_img = ImageEnhancement(normalized)


    # Calculating 2D-Gabor Wavelets

    filter1, _ = defined_gabor(enhanced_img, 0.4, 3, 1.5)
    filter2, _ = defined_gabor(enhanced_img, 0.4, 4.5, 1.5)
    bitblock1 = getBitBlocks(filter1, size = 8)
    bitblock2 = getBitBlocks(filter2, size = 8)

    bitblock1 = bitblock1.reshape(bitblock1.shape[0]//16, 16)
    bitblock2 = bitblock2.reshape(bitblock2.shape[0]//16, 16)

    # Plotting the result of outer iris boundary

    h,w, _ = exampleArray.shape
    out = exampleArray.copy()[:,(w - h)//2:(w + h)//2,:]
    cv2.circle(out, iris_center, iris_rad, (0, 0, 255), 1)
    cv2.circle(out, (pupil_center[0]+iris_center[0]-iris_rad, pupil_center[1]+iris_center[1]-iris_rad), pupil_rad, (0, 0, 255), 1)


    fig, ax = plt.subplots(2,3, figsize = (10,10))

    ax[0,0].imshow(out[::,::,::-1])
    #plt.xticks(np.round(np.linspace(0,out.shape[1],10)))
    pupil_out = np.repeat(pupil_crop[:, :, np.newaxis], 3, axis=2)

    cv2.circle(pupil_out, pupil_center, pupil_rad, (0, 0, 255), 1)
    cv2.circle(pupil_out, (pupil_out.shape[0]//2,pupil_out.shape[1]//2), iris_rad, (0, 0, 255), 1)
    ax[1,0].imshow(pupil_out[::,::,::-1], cmap = 'gray')
    ax[0,1].imshow(enhanced_img, cmap = 'gray')
    ax[1,1].imshow(normalized, cmap = 'gray')
    fig.suptitle(str.split(path,'\\')[-1])

    #ax[0,2].imshow(filter1, cmap = 'gray')
    #ax[1,2].imshow(filter2, cmap = 'gray')
    ax[0,2].imshow(bitblock1)
    ax[1,2].imshow(bitblock2)
    #ax[2,2].imshow(np.abs(bitblock1 - bitblock2))


    #print(path)
    Path().mkdir(parents=True, exist_ok=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(current_dir, 'OutputDataNew\\')
    individualIdx, leftOrRight, imageName = str.split(path,'\\')[-3:]
    imageName = str.split(imageName, '.')[0]
    #print(individualIdx)
    #print(leftOrRight)
    #print(imageName)
    out_dir = out_dir + individualIdx + '\\' + leftOrRight +'\\'
    #print(str(out_dir))
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    if saveResults:
        plt.savefig(out_dir + imageName + '.pdf')
        np.save(out_dir + imageName + '.npy', normalized)
    if closeFigAfter:
        plt.close(fig)
    return fig



if __name__ == '__main__':
    

    
    imagePaths = getDatasetImagePaths()
    #imagePaths[individual_idx][left/right_idx][sample_idx]
    
    #path = imagePaths[9][1][4]
    #fig = computeNormalizedIrisAndSave(path, closeFigAfter=False, saveResults = False)
    #plt.show()

    unwrappedImagePaths = [imagePath for person in imagePaths
                                        for leftRight in person
                                            for imagePath in leftRight]
    with Pool() as p:
        r = list(tqdm(p.imap(computeNormalizedIrisAndSave, unwrappedImagePaths), total = len(unwrappedImagePaths)))
