import uvicorn as uvicorn
from fastapi import FastAPI, Response, Request, HTTPException
import calc

app = FastAPI()

@app.get("/sitemap.xml")
async def get_sitemap():

    with open('scheme.xml') as inputfile: # Открываем файл с xml-содержимым
        xml_file = inputfile.read() # Записываем содержимое в переменную

    return Response(content=xml_file, media_type="application/xml")


@app.post("/submit.xml")
async def submit(request: Request):

    content_type = request.headers['Content-Type']
    if content_type == 'application/xml':
        body = await request.body()
        #декодировка запроса в байтах
        
        my_body=body.decode('utf-8')
        #запись полученных данных в рабочий xml
        myfile = open("items.xml", "w")
        myfile.write(my_body)
        myfile.close()

        SC_place = str(request._query_params)
        SC_place = SC_place[:-1]
        
        I_kz=str(calc.Ikz("items2.xml",SC_place))

        return Response(content=I_kz, media_type="application/xml")
    else:
        raise HTTPException(status_code=400, detail=f'Content type {content_type} not supported')

if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=8000)
