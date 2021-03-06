from django.shortcuts import render,redirect
from django.core import serializers
# .models 현재 폴더 모델의 Article
from django.http.response import HttpResponse
from .models import Movie, Theater, Room, TheaterMovie, Timetable
from .CGVMovieInfoParsing import CGVMovieInfo
from .LotteMovieInfoParsing import LOTTEMovieInfo
from .MEGABOXMovieInfoParsing import MEGABOXMovieInfo
from multiprocessing.pool import ThreadPool
import simplejson as json
from datetime import date, datetime,timedelta
# DRF
# Create your views here.


def viewMovieInfoByBranch(request):
    requestResult = dict(request.POST)
    try:
        CGVBranchs = requestResult['CGV']
    except:
        CGVBranchs = []

    try:
        LotteBranchs = requestResult["Lotte"]
    except:
        LotteBranchs = []

    try:
        MEGABOXBranchs = requestResult["MEGABOX"]
    except:
        MEGABOXBranchs = []

    CGVNormalInfo, CGVSpecialInfo, LotteNormalInfo, LotteSpecialInfo, MEGABOXNormalInfo, MEGABOXSpecialInfo = \
        searchByBranch(CGVBranchs, LotteBranchs, MEGABOXBranchs)
    context = {
        'CGV_normal_info': CGVNormalInfo,
        'CGV_special_info': CGVSpecialInfo,
        'Lotte_normal_info': LotteNormalInfo,
        'Lotte_special_info': LotteSpecialInfo,
        'MEGABOX_normal_info': MEGABOXNormalInfo,
        'MEGABOX_special_info': MEGABOXSpecialInfo,
    }

    return render(request, 'viewMovieInfoByBranch.html', context)


def selectBranch(request):
    CGV_branchs = set()
    Lotte_branchs = set()
    MEGABOX_branchs = set()
    
    Branchs = Theater.objects.all()
    Branch_location_info = []
    for branch in Branchs:
        if branch.company == "CGV":
            CGV_branchs.add(branch.branch)
        elif branch.company == "MEGABOX":
            MEGABOX_branchs.add(branch.branch)
        elif branch.company == "Lotte":
            Lotte_branchs.add(branch.branch)

        branch_info = {
            'company' : branch.company,
            'name' : branch.branch,
            'lat' : branch.lat,
            'lon' : branch.lon,
        }
        Branch_location_info.append(branch_info)

    context = {
        'CGV_branchs': CGV_branchs,
        'Lotte_branchs': Lotte_branchs,
        'MEGABOX_branchs': MEGABOX_branchs,
        'branchs_locations' : json.dumps(Branch_location_info)
    }

    return render(request, "selectBranch.html", context)


def searchByBranch(CGVBranchs, LotteBranchs, MEGABOXBranchs):
    CGVInfo = CGVMovieInfo()
    LotteInfo = LOTTEMovieInfo()
    MEGABOXInfo = MEGABOXMovieInfo()

    CGVBranchLen = len(CGVBranchs)
    LotteBranchLen = len(LotteBranchs)
    MEGABOXLen = len(MEGABOXBranchs)
    pool = ThreadPool(CGVBranchLen + LotteBranchLen + MEGABOXLen + 2)
    results = []
    trash = 0

    CGVNormalInfo = []
    CGVSpecialInfo = []
    for branch in CGVBranchs:
        results.append(pool.apply_async(CGVInfo.CGVCrawingInfo,
                                        (branch, CGVInfo.CGV_branch[branch], CGVNormalInfo,
                                         CGVSpecialInfo)))  # tuple of args for foo)


    LotteNormalInfo = []
    LotteSpecialInfo = []

    for branch in LotteBranchs:
        results.append(pool.apply_async(LotteInfo.LOTTENomalCrawingInfo,
                                        (branch, LotteInfo.Lotte_branch[branch],
                                         LotteNormalInfo)))  # tuple of args for foo)

    results.append(pool.apply_async(LotteInfo.LOTTEspecialCrawingInfo, (trash, LotteSpecialInfo)))

    MEGABOXNormalInfo = []
    MEGABOXSpecialInfo = []

    for branch in MEGABOXBranchs:
        results.append(pool.apply_async(MEGABOXInfo.MEGABOXNomalCrawingInfo,
                                        (branch, MEGABOXInfo.MEGABOX_branch[branch],
                                         MEGABOXNormalInfo)))  # tuple of args for foo)

    results.append(pool.apply_async(MEGABOXInfo.MEGABOXSpecialCrawingInfo, (trash, MEGABOXSpecialInfo)))

    results = [r.get() for r in results]

    return CGVNormalInfo, CGVSpecialInfo, LotteNormalInfo, LotteSpecialInfo, MEGABOXNormalInfo, MEGABOXSpecialInfo


def index(request):
    CGVInfo = CGVMovieInfo()
    LotteInfo = LOTTEMovieInfo()
    MEGABOXInfo = MEGABOXMovieInfo()

    # CGVNormalInfo, CGVSpecialInfo, LotteNormalInfo, LotteSpecialInfo, MEGABOXNormalInfo, MEGABOXSpecialInfo = \
    #     searchByBranch(CGVInfo.CGV_branch, LotteInfo.Lotte_branch, MEGABOXInfo.MEGABOX_branch)

    # inputDatasToDB(CGVNormalInfo)
    # inputDatasToDB(CGVSpecialInfo)
    # inputDatasToDB(LotteNormalInfo)
    # inputDatasToDB(LotteSpecialInfo)
    # inputDatasToDB(MEGABOXNormalInfo)
    # inputDatasToDB(MEGABOXSpecialInfo)
    
    return render(request, 'index.html')

def findbylocate(request):
    data = dict(request.GET)
    try:
        CGV = data['CGV']
        CGVtheaters = Theater.objects.filter(company="CGV",branch__in=CGV)
    except:
        CGVtheaters = Theater.objects.none()
    try:
        MEGABOX = data['MEGABOX']
        MEGABOXtheaters = Theater.objects.filter(company="MEGABOX",branch__in=MEGABOX)

    except:
        MEGABOXtheaters = Theater.objects.none()
    try:
        LOTTE = data['Lotte']
        LOTTEtheaters = Theater.objects.filter(company="Lotte",branch__in=LOTTE)
    except:
        LOTTEtheaters = Theater.objects.none()
    theaters = CGVtheaters | MEGABOXtheaters | LOTTEtheaters
    theaters_id = []
    for theater in theaters:
         theaters_id.append(theater.id)
    theatermovies = TheaterMovie.objects.filter(theater_id__in=theaters_id)
    context = {
        'theatermovies' : theatermovies,
    }
    return render(request, 'locateresult.html',context)

def findbyname(request):
    if request.GET.get("type") == "title":
        title = request.GET.get("title")    
        theaters = Movie.objects.get(title=title).theaters.all()
        remain_count = 5-theaters.count()%5
        context = {
            'theaters' : theaters,
            'remain_count' : range(remain_count),
        }
        return render(request, 'categorypage.html', context)
    else:
        id_string = request.GET.get('selected')
        movie_id = id_string.split('-')[0]
        theater_id = list(map(int,id_string.split('-')[1:-1]))
        movie_title = Movie.objects.get(id=movie_id).title
        theaters = Theater.objects.filter(id__in=theater_id)
        theatermovies = TheaterMovie.objects.filter(movie_id=movie_id, theater_id__in=theater_id)
        print()
        context = {
            'theatermovies' : theatermovies,
        }
        return render(request,'nameresult.html', context)

def findmoviename(request):
    movies = Movie.objects.all().values('title', 'id')
    remain_count = 5-movies.count()%5
    context = {
        'remain_count' : range(remain_count),
        'movies' : movies,
    }
    return render(request, 'findnamepage.html', context)

def inputDatasToDB(datas):
    today = date.today()
    room_id = -1
    movie_id = -1
    room = ""
    movie = ""
    print(today)
    for data in datas:
        room_id,movie_id,room,movie = inputCrawlingDataToDB(data,today,room_id,movie_id,room,movie)

def inputCrawlingDataToDB(CrawlingData,today,room_id,movie_id,room_temp,movie_temp):
    # print(CrawlingData)
    theater= Theater.objects.get(company=CrawlingData['company'],branch=CrawlingData['branch'])
    if movie_temp ==CrawlingData['movie'] :
        movie = movie_id
    else:
        movie, created = Movie.objects.update_or_create(
            title = CrawlingData['movie'], 
            defaults={
                'title' : CrawlingData['movie']
            }
        )

    if room_temp == CrawlingData['hall']:
        room = room_id
    else :
        room, created = Room.objects.update_or_create(
            theater_id = theater.id,
            name = CrawlingData['hall'],
            category = CrawlingData['special'],
            defaults={
                'theater_id' : theater.id,
                'name' : CrawlingData['hall'],
                'category' : CrawlingData['special'],
            }
        )
    theatermovie, created = TheaterMovie.objects.update_or_create(
        theater_id = theater.id,
        movie_id = movie.id,
        defaults={
            'theater_id' : theater.id,
            'movie_id' : movie.id,
        }
    )
    d1 = today.strftime("%Y-%m-%d")

    start_time = " ".join([d1,CrawlingData['time']])
    
    try:
        date_time = datetime.strptime(start_time,'%Y-%m-%d %H:%M')
    except:
        d1 = (today + timedelta(hours=1)).strftime("%Y-%m-%d")
        time = CrawlingData['time'].split(":")
        hour = time[0]
        minute = time[1]
        time = str((int(hour)-24))+":"+minute
        start_time = " ".join([d1,time])
        date_time = datetime.strptime(start_time,'%Y-%m-%d %H:%M')

    timetable, created = Timetable.objects.update_or_create(
        start_time = date_time,
        room_id = room.id,
        link = CrawlingData['link'],
        defaults={
            'start_time' : date_time,
            'room_id' : room.id,
            'playInfo_id' : theatermovie.id,
            'remainSeat' : CrawlingData['remainSeat'],
            'link' : CrawlingData['link'],
        }
    )
    return room,movie,CrawlingData['hall'],CrawlingData['movie']


def adminpage(request):
    if request.user.is_staff:
        if request.method == "POST":
                theater, created = Theater.objects.update_or_create(
                    company = request.POST.get("company"), 
                    branch = request.POST.get("branch"),
                    defaults={
                        'company' : request.POST.get("company"),
                        'branch' : request.POST.get("branch"), 
                        'lat' : request.POST.get("lat"), 
                        'lon' : request.POST.get("lon"),
                        }
                )

                movie, created = Movie.objects.update_or_create(
                    title = request.POST.get("title"), defaults={
                        'title' : request.POST.get("title"),
                    }
                )
                room, created = Room.objects.update_or_create(
                    theater_id = theater.id,
                    name = request.POST.get("name"),
                    defaults={
                        'theater_id' : theater.id,
                        'name' : request.POST.get("name"),
                        'category' : request.POST.get("category"),
                    }
                )
                theatermovie, created = TheaterMovie.objects.update_or_create(
                    theater_id = theater.id,
                    movie_id = movie.id,
                    defaults={
                        'theater_id' : theater.id,
                        'movie_id' : movie.id,
                    }
                )
                start_time_date = request.POST.get("start_time_date")
                start_time_time = request.POST.get("start_time_time")
                start_time = " ".join([start_time_date,start_time_time])
                timetable, created = Timetable.objects.update_or_create(
                    start_time = start_time,
                    room_id = room.id,
                    defaults={
                        'start_time' : start_time,
                        'room_id' : room.id,
                        'playInfo_id' : theatermovie.id,
                    }
                )

                return redirect('board:adminpage')
        else:
            theaters = Theater.objects.all().order_by("-created_at")
            # for theater in theaters:
            #     print(theater.get_all_movies)
            #     print(theater.movies.all())
                
            #     for movie in theater.movies.all():
            #         print(theater.movies.all())
            #         print(movie.title)
            context = {
                'theaters' : theaters,
            }
            return render(request, 'adminpage.html', context)
    else:
        return redirect('accounts:signin')    

def theater_delete(request):
    theater_id = request.POST["theater_id"]
    theater = Theater.objects.get(id=theater_id)
    if request.user.is_staff:
        theater.delete()
        context = {
                'theater_id' : theater_id,
            }
        return HttpResponse(json.dumps(context), status=200, content_type="application/json")
    else:
        return HttpResponse(status=401)
