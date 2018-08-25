def minsToDegrees (minsString, isLongitude):
    parts = minsString.split("-")

    parts[0] = float(parts[0])
    parts[1] = float(parts[1])
    parts[2] = float(parts[2][:parts[2].find(" ")])

    degrees = parts[0] + (parts[1] / 60) + (parts[2] / 3600)

    if isLongitude:
        degrees *= -1

    return degrees


testString = "118-16-31.54 W"
print minsToDegrees(testString, True)
