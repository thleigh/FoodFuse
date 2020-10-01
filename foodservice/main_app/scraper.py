# from asgiref.sync import sync_to_async
# from .doordash import doordash, doordash_unparsed_list, parsed_data
# from .postmates import postmates, postmates_unparsed_list, postmates_data
# import asyncio, time
# from .forms import SearchForm, RestaurantForm, FavoriteForm

# async def scraper_function(request):
#     location = request.session.get('location')
#     print('Hello World')
#     task1 = asyncio.ensure_future(doordash(location))
#     task2 = asyncio.ensure_future(postmates(location))
#     await asyncio.wait([
#         task1, task2
#     ])
#     # return render(request, '/scraper_function')
#     return HttpResponseRedirect('/data/')

# def data(request):
#     final_dd_data = []
#     final_pm_data = []
#     for dd_data in doordash_unparsed_list:
#         parsed_data(dd_data)
#         if "Currently Closed" in doordash_unparsed_list:
#             pass
#         else:
#             final_dd_data.append(parsed_data.results)
#     postmates_list = [x for x in postmates_unparsed_list if x]
#     for pm_data in postmates_list:
#         postmates_data(pm_data)
#         final_pm_data.append(postmates_data.results)
#     forms = RestaurantForm()

#     return render(request, 'data.html', {
#         'doordash': final_dd_data, 
#         'postmates': final_pm_data,
#     })