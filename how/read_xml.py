
import xml.etree.ElementTree as ET
import os
base='/home/ubuntu/local/mitsubishi_dataset/png_images'
s = '/home/ubuntu/local/mitsubishi_dataset/annotation'
dic_list=[]
qdic=[]
idic=[]
j=0
for d in os.listdir(s):
    label_name= d
    sorce = os.path.join(s,d)
    dir = os.listdir(sorce)
    for i in range(len(dir)):
        if i%5==0:
            if '.xml' in dir[i]:
                tree = ET.parse(sorce + '/' + dir[i])
                rect = {}
                line = ""
                root = tree.getroot()
                with open('m_label_test.txt', 'a', encoding='utf-8') as f1:
                    for name in root.iter('path'):
                        rect['path'] = name.text
                    for ob in root.iter('object'):

                        for bndbox in ob.iter('bndbox'):
                            dic={}
                            l=[]
                            j=j+1
                            # for l in bndbox:
                            #     print(l.text)
                            for xmin in bndbox.iter('xmin'):
                                rect['xmin'] = xmin.text
                                l.append(float(rect['xmin']))
                            for ymin in bndbox.iter('ymin'):
                                rect['ymin'] = ymin.text
                                l.append(float(rect['ymin']))
                            for xmax in bndbox.iter('xmax'):
                                rect['xmax'] = xmax.text
                                l.append(float(rect['xmax']))
                            for ymax in bndbox.iter('ymax'):
                                rect['ymax'] = ymax.text
                                l.append(float(rect['ymax']))
                            f_name=rect['path'].split('/')[5]
                            i_name=rect['path'].split('/')[6]
                            final_path=os.path.join(base,f_name,i_name)
                            #print(final_path)
                            dic['image']=final_path
                            dic['bbx']=l
                            dic['id']=j
                            #print(rect['xmin'] + ' ' + rect['ymin'] + ' ' + rect['xmax'] + ' ' + rect['ymax'])

                            line = rect['xmin'] + ' ' + rect['ymin'] + ' ' + rect['xmax'] + ' ' + rect['ymax'] + " "
                            f1.write(line)
                            
                            for t in ob.iter('name'):
                                dic['label']=t.text
                                #print(t.text)
                            
                                f1.write(t.text + '\n')
                    qdic.append(dic)
        else:
            if '.xml' in dir[i]:
                tree = ET.parse(sorce + '/' + dir[i])
                rect = {}
                line = ""
                root = tree.getroot()
                with open('m_label_test.txt', 'a', encoding='utf-8') as f1:
                    for name in root.iter('path'):
                        rect['path'] = name.text
                    for ob in root.iter('object'):

                        for bndbox in ob.iter('bndbox'):
                            dic={}
                            l=[]
                            j=j+1
                            # for l in bndbox:
                            #     print(l.text)
                            for xmin in bndbox.iter('xmin'):
                                rect['xmin'] = xmin.text
                                l.append(float(rect['xmin']))
                            for ymin in bndbox.iter('ymin'):
                                rect['ymin'] = ymin.text
                                l.append(float(rect['ymin']))
                            for xmax in bndbox.iter('xmax'):
                                rect['xmax'] = xmax.text
                                l.append(float(rect['xmax']))
                            for ymax in bndbox.iter('ymax'):
                                rect['ymax'] = ymax.text
                                l.append(float(rect['ymax']))
                            f_name=rect['path'].split('/')[5]
                            i_name=rect['path'].split('/')[6]
                            final_path=os.path.join(base,f_name,i_name)
                            #print(final_path)
                            dic['image']=final_path
                            #print(dic['image'])
                            dic['bbx']=l
                            dic['id']=j
                            #print(rect['xmin'] + ' ' + rect['ymin'] + ' ' + rect['xmax'] + ' ' + rect['ymax'])

                            line = rect['xmin'] + ' ' + rect['ymin'] + ' ' + rect['xmax'] + ' ' + rect['ymax'] + " "
                            f1.write(line)
                            
                            for t in ob.iter('name'):
                                dic['label']=t.text
                                #print(t.text)
                            
                                f1.write(t.text + '\n') 
                            #print(dic)
                    idic.append(dic)
        dic_list.append(dic)
        #print(dic_list)
#print(dic_list[0:4])
