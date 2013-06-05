import install
import unittest
import os
import shutil

class TestInstallFunctions(unittest.TestCase):

  def setUp(self):
    os.mkdir('templates/tmp')

  def tearDown(self):
    shutil.rmtree('templates/tmp')
    
  def test_string_to_file(self):
    text="""\
    Una\
    Prueba\
    """
    filename='/tmp/test_string_to_file'
    install.string_to_file(text,filename)
    file_created=open(filename,'r')
    readed_text=file_created.read()
    self.assertEqual(text,readed_text)
    file_created.close()

  def test_create_file_from_template(self):
    text="Este es un {{t}}!!!"
    template_file_name='tmp/test_create_file_from_template'
    template_file=open('templates/%s'%template_file_name,'w')
    template_file.write(text);
    template_file.close()
    created_file_name='/%s'%template_file_name
    install.create_file_from_template(created_file_name,{'t':'template'})
    created_file=open(created_file_name,'r')
    text_from_created_file=created_file.read()
    created_file.close()
    self.assertEqual(text_from_created_file,"Este es un template!!!")

  def test_backup_file(self):
    filename = '/tmp/test_backup_file'
    open(filename,'w').close()
    install.backup_file(filename)
    self.assertTrue(os.path.exists('%s.default'%filename))

    
