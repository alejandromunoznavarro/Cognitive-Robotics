# tools useful for a robot which would like to use a camera to follow a
# line

def findLineDeviation(imageGray):
  """
  This takes a grayscale image and applies a threshold (GRAY_THRESHOLD)
  to the center SEARCH_HEIGHT rows of pixels.  Next it combines those
  rows into one row keeping the maximum pixel value in each column and
  then calculates the center of mass of the line's pixels.  It returns
  whether a line was found (True/False) and the deviation (a float in
  the range of -1 to 1) with respect to the center column of the image.  
  
  A deviation of 0 means that the line is centered.  A deviation of 1
  means that the line is on the right edge of the image, a deviation of
  -1 means that the line is on the left.  Intermediate values are
  proportional to the line's position.
  
  NOTE: This will not work correctly if there is more than one line in
  the SEARCH_HEIGHT rows; it will just return the center of mass of
  every line's pixels.  Also it will not work as expected when the line
  is nearly horizontal.  In fact, a completely horizontal line will have
  a deviation of 0.
  """
  
  GRAY_THRESHOLD = 50
  SEARCH_HEIGHT = 4

  # if there are three arguments, the third gives the number of channels
  if (len(imageGray.shape)>2):
    # it isn't a grayscale image!
    print ("Error: input to findLineDeviation not in grayscale format.")
    return False, 0
  
  # only keep threshold values of at most the middle SEARCH_HEIGHT
  # rows of pixels
  middleRowIndex = imageGray.shape[0]//2
  if (middleRowIndex>=SEARCH_HEIGHT//2):
    lineData = imageGray[middleRowIndex-(SEARCH_HEIGHT//2):
                         middleRowIndex+(SEARCH_HEIGHT//2-1),
                          :] < GRAY_THRESHOLD
  else:
    lineData = imageGray < GRAY_THRESHOLD
  # combine the rows keeping the max in each column
  thresholds = lineData.max(axis=0)
  # count the number of line pixels found
  lineCount = thresholds.sum()
  
  # if we found a line, calculate the centroid then the error
  if(lineCount>0):
    centerColumnIndex = thresholds.shape[0]//2
  
    # use the idexes as weights to calculate centroid
    weights = thresholds*range(-centerColumnIndex,
                               centerColumnIndex+(thresholds.shape[0]%2))
    error = weights.sum()/lineCount/centerColumnIndex

    return True, error
  else:
    return False, 0
