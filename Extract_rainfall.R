library(raster)
library(rgdal)
lats <- c(12.14627)
lons <- c(78.00722)
ras.files <- Sys.glob("/media/edrive1/Shashank/shashank_Mount/Extract_Rainfall/*.tif")
bn <- strsplit(basename(ras.files),".tif")
ras.fle <- ras.files[bn>=20200101 & bn <= 20211231]


in.dates <- as.Date(basename(ras.fle), '%Y%m%d')

m <- length(lats)
n <- length(ras.fle)
out.file <- '/media/edrive1/Shashank/shashank_Mount/csv/1616.csv'
rf.vals <- c()
for(i in 1:n){
  ras <- raster(ras.fle[i])
  rf.val <- extract(ras, cbind(lons, lats))
  rf.vals <- append(rf.vals, rf.val)
  print(i)
}

out.df <- data.frame(Date = in.dates, Rainfall = round(rf.vals,2))
write.csv(out.df, out.file, row.names = F)


