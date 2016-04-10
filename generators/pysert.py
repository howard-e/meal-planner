'''
@license:
Copyright 2011 Andrei N. Ciobanu

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from abc import abstractmethod as abstractclassmethod
import abc
import argparse
import random
import re
import string
import sys
import textwrap
import datetime

from xml.etree.ElementTree import ElementTree


# ------------------------------------------------------------------------------
class AbstractDataSet(object):
    '''
    Abstract class base for data sets .
    Classes based on AbstractDataSet are dynamic and must implement
    next_value() method .
    '''

    __metaclass__ = abc.ABCMeta

    @abstractclassmethod
    def validation_list(self):
        return [];

    def validate(self):
        valid = True
        vl_list = self.validation_list();

        for elem in vl_list:
            if elem not in self.__dict__.keys():
                sys.stderr.write('Error: Invalid data set : \'%s\' .\n' %
                                 self.name)
                sys.stderr.write('Error: Missing property \'%s\' .\n' %
                                 elem)
                sys.stderr.write('Exiting (-1).\n')
                sys.exit(-1)

    def __init__(self, ds_dict):
        '''
        Subclasses will have a dynamic structure based on the
        ds_dict dictionary .
        '''
        for (k, v) in ds_dict.items():
            self.__dict__[k] = v
        # validate data set based on validation_list
        self.validate()

    @abc.abstractmethod
    def next_value(self):
        return


# ------------------------------------------------------------------------------
class RandomNumber(AbstractDataSet):
    '''
    ds_dict will contain the following:
            {
                "name" : <string value>
                "floating" : "<boolean value>" ,
                "min": "<integer value>",
                "max": "<integer value>"
            }
    '''

    def validation_list(self):
        return ['name', 'floating', 'min', 'max']

    def next_value(self):
        '''
        Returns a random value based on in the ds_dict properties .
        '''
        func = random.uniform if self.floating == 'True' else random.randint
        return func(int(self.min), int(self.max))


# ------------------------------------------------------------------------------
class LoremIpsum(AbstractDataSet):
    '''
    ds_dict will contain the following :
        {
            "name" : <string value>
            "length" : "<integer value>"
        }
    '''

    lorem_impsum = textwrap.dedent('''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut quis justo leo.
    Quisque congue elit eu ante euismod ut aliquam nisi bibendum. Donec mollis
    ipsum nec sapien auctor ut blandit ante aliquet. Fusce eget ante nunc.
    Praesent ullamcorper neque sit amet diam scelerisque condimentum. Nulla
    faucibus, justo non pretium consequat, tortor ligula consequat elit, vitae
    dapibus orci metus eget nisl. Fusce ante ante, placerat et gravida ac,
    fermentum eu nisl. Aenean posuere, orci vel dapibus adipiscing, ipsum dui
    imperdiet dolor, eu rutrum lorem dolor id felis. Curabitur accumsan enim et
    ipsum volutpat feugiat. Vivamus eget diam eros, in volutpat justo.
    Curabitur bibendum, velit ac fermentum tincidunt, dui nulla volutpat nulla,
    in ornare dui turpis ultrices dolor. Sed gravida suscipit arcu, ut
    scelerisque augue aliquet non. Sed sagittis, turpis id ullamcorper rhoncus,
    lorem nisi fringilla leo, et tristique odio augue id tortor. Integer
    vehicula imperdiet nisl, eu ultrices neque condimentum eu. Ut sed purus
    diam, eu euismod diam. Fusce eget venenatis arcu. Mauris porta, enim vel
    pretium sagittis, ligula elit rutrum magna, sed pulvinar orci elit sit amet
    leo. Pellentesque habitant morbi tristique senectus et netus et malesuada
    fames ac turpis egestas.
    ''').strip().replace('\n', '')

    def validation_list(self):
        return ['name', 'length']

    def next_value(self):
        '''
        Returns a lorem ipsum text .
        '''
        div = int(int(self.length) / len(LoremIpsum.lorem_impsum))
        mod = int(self.length) % len(LoremIpsum.lorem_impsum)
        return div * LoremIpsum.lorem_impsum + LoremIpsum.lorem_impsum[:mod]


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
class PersonName(AbstractDataSet):
    '''
    ds_dict will contain the following :
        {
            "name" : <string value>
            "firstname" : "<boolean value>",
            "lastname" : "<boolean value>"
        }
    '''

    ''' Popular first names in 2010 '''
    fname = ['Ava', 'Aaron', 'Agathe', 'Agnes', 'Alba', 'Alexander', 'Alexis',
             'Alvaro', 'Andrew', 'Andrei', 'Angelina', 'Anthony', 'Anna', 'Ariana',
             'Brian', 'Bogdan', 'Carmen', 'Cristopher', 'Connor', 'Daan',
             'Daniel', 'David', 'Diego', 'Ella', 'Elizabeth', 'Elsa',
             'Emma', 'Enzo', 'Ethan', 'Gabriel', 'Grace', 'Gustav',
             'Isaac', 'Jacob', 'Javier', 'Jayden', 'John', 'Juliette',
             'Kacper', 'Lars', 'Leah', 'Levi', 'Logan', 'Lotte', 'Lucas',
             'Lieke', 'Linus', 'Lucia', 'Mateusz', 'Maxime', 'Melvin',
             'Mia', 'Michael', 'Mikolaj', 'Milan', 'Natalie', 'Natalia',
             'Olivia', 'Oscar', 'Pablo', 'Paul', 'Paula', 'Piotr', 'Quentin',
             'Sarah', 'Samuel', 'Sophia', 'Sem', 'Szymon', 'Thijs', 'Teodore',
             'Valeria', 'Valter', 'William', 'Wilma']

    ''' Last names '''
    lname = ['Abbott', 'Alcott', 'Antonescu', 'Bartok', 'Bayard', 'Banciu',
             'Bethmann', 'Bergen', 'Botev', 'Brown', 'Bush', 'Corvinus',
             'Chehachkov', 'Dimitrof', 'Dinev', 'Delano', 'Eisenhower', 'Enescu',
             'Frels', 'Fugger', 'Gilman', 'Hancock', 'Hoza', 'Ionescu', 'Iordache',
             'Kalish', 'Kafka', 'Krasniki', 'Lukasewicz', 'McCormick', 'Medici',
             'Menier', 'Morgan', 'Palagyi', 'Parrocel', 'Romanov', 'Rozycki',
             'Rufus', 'Olaru', 'Otis', 'Schoenberger', 'Strauss', 'Somoza',
             'Sowinski', 'Szigete', 'Tessedik', 'Tisch', 'Vajda', 'Vlas',
             'Walker', 'Warhola', 'Varchol', 'Wojnar', 'Zelenjcik']

    def validation_list(self):
        return ['name', 'firstname', 'lastname']

    def next_value(self):
        '''
        Returns a random string based on ds_dict properties
        '''
        ret = ''
        if self.firstname == 'True':
            fname_idx = random.randint(0, 1000) % len(self.fname)
            ret = ret + self.fname[fname_idx]
        if self.lastname == 'True':
            lname_idx = random.randint(0, 1000) % len(self.lname)
            if len(ret) > 0:
                ret = ' ' + ret
            ret = ret + self.lname[lname_idx]
        return ret


# ------------------------------------------------------------------------------
class Sequence(AbstractDataSet):
    '''
     ds_dict will contain the following:
        {
            "name" : <string value>
            "start" : "<integer value>",
            "increment" : "<integer value>"
        }
    '''

    def __init__(self, ds_dict):
        '''
        We will need to @override the constructor in order to add
        the _cval property (current value in sequence) .
        '''
        super(Sequence, self).__init__(ds_dict)
        self.__cval = int(self.start) - int(self.increment)

    def validation_list(self):
        return ['name', 'start', 'increment']

    def next_value(self):
        '''
        Returns the next value in the sequence by adding the increment to
        the current value
        '''
        self.__cval += int(self.increment)
        return self.__cval


# -----------------------------------------------------------------------------
class NumberSequence(AbstractDataSet):
    '''
     ds_dict will contain the following:
        {
            "name" : <string value>
            "length" : "<integer value>",
        }
    '''
    seen = set()

    def validation_list(self):
        return ['name', 'length']

    def next_value(self):
        if (int(self.length) <= 0):
            return ''
        p = [str(random.randint(1, 9))]
        p.extend(str(random.randint(0, 9)) for i in xrange(int(self.length) - 1))
        p = ''.join(p)
        return p


# ------------------------------------------------------------------------------
class AlphaNumeric(AbstractDataSet):
    '''
     ds_dict will contain the following:
        {
            "name" : <string value>
            "min_length" : <long value>
            "max_length" : <long value>
            "alphabet" : <boolean value>
            "numeric" : <boolean value>
        }
    '''
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    number = "0123456789"

    def validation_list(self):
        return ["name", "min_length", "max_length", "alphabet", "numeric"]

    def next_value(self):
        lst = ""
        if self.alphabet == "True":
            lst += self.alpha
        if self.numeric == "True":
            lst += self.number
        return ''.join(lst[random.randint(0, 1000) % len(lst)] for i in
                       xrange(random.randint(int(self.min_length), int(self.max_length))))


# ------------------------------------------------------------------------------
class Date(AbstractDataSet):
    '''
     ds_dict will contain the following:
        {
            "name" : <string value>
            "max_year" : "<int value>",
            "min_year" : "<int value>"
        }
    '''

    def validation_list(self):
        return ["name", "max_year", "min_year"]

    def next_value(self):
        self.max_year = min(9999, int(self.max_year))
        self.min_year = max(1, int(self.min_year))
        if self.max_year == self.min_year:
            return datetime.date.today().isoformat()
        if self.max_year < self.min_year:
            return datetime.date.today().isoformat()
        dt = datetime.date(random.randint(self.min_year, self.max_year), random.randint(1, 12),
                           random.randint(1, 28))
        return dt.isoformat()


# ------------------------------------------------------------------------------
class RandomFoodImage(AbstractDataSet):
    '''
    ds_dict will contain the following:
        {
            "name" : <string value>
        }
    '''

    ''' Random food images from Google '''
    food_img_list = [
        'http://cdn.playbuzz.com/cdn/89c9243a-e0cd-495e-90e0-11642327f13f/f4b834c8-a506-43f5-8c2c-3e125311275c_560_420.jpg',
        'http://images2.fanpop.com/images/photos/5400000/Random-Food-random-5409310-1280-800.jpg',
        'http://images4.fanpop.com/image/photos/23600000/creative-food-3-random-23639450-500-333.jpg',
        'http://photos1.blogger.com/blogger/3914/618/1600/untitled1.JPG',
        'http://www.hangukdrama.com/wp-content/uploads/2012/11/IMG_4526.jpg',
        'http://images2.fanpop.com/images/photos/5400000/Random-Food-random-5409303-1280-800.jpg',
        'http://40.media.tumblr.com/bbe6be2ef523c45a694cd570eb4d7deb/tumblr_inline_nocovf6iGQ1s9623o_500.jpg',
        'https://images.rapgenius.com/ce46193adc445413cb49e35c0cefbb90.1000x669x1.jpg',
        'http://stupiddope.com/wp-content/uploads/2014/04/gold-plated-grilled-cheese-sandwich-1.jpg',
        'http://images2.fanpop.com/images/photos/5400000/Random-Food-random-5409295-1280-800.jpg',
        'http://melissadreamsofsushi.com/wp-content/uploads/2013/11/IMG_3490.jpg',
        'http://static.giantbomb.com/uploads/original/11/118908/2646473-6885497418-sicil.jpg',
        'http://3.bp.blogspot.com/_VF64TeUDSR0/TSxboB_zruI/AAAAAAAAABY/rlNIAyYNS3E/s1600/bacon-wrapped-hot-dog-maple-bar.jpg',
        'http://www.hungryhungryhippie.com/wp-content/uploads/2014/12/IMG_0887.jpg',
        'http://2.bp.blogspot.com/-JRaJSeLq3Sw/Ui8FbMPm6yI/AAAAAAAAHh4/F_uZh6hrG2U/s1600/01+Candy+Show+Time.JPG']

    def validation_list(self):
        return ['name']

    def next_value(self):
        return random.choice(self.food_img_list)


# ------------------------------------------------------------------------------
class RandomIngredient(AbstractDataSet):
    '''
    ds_dict will contain the following:
        {
            "name" : <string value>
            "result" : <string value>
        }
    '''

    ''' Random food ingredients '''
    ingredient_type_list = ['curry powder', 'succotash', 'heavy cream', 'tofu', 'leeks', 'raw sugar',
                            'cream of tartar', 'dried leeks', 'cranberries', 'pig\'s feet', 'lemon juice',
                            'rabbits', 'peaches', 'black-eyed peas', 'onion powder', 'coriander', 'cannellini beans',
                            'tortillas', 'chickpeas', 'green beans', 'wine', 'brandy', 'brown rice',
                            'orange peels', 'cider vinegar', 'haddock', ' wine vinegar', 'spinach', 'amaretto',
                            'chard', 'brunoise', 'oatmeal', 'navy beans', 'berries', 'cooking wine', 'corn syrup',
                            'mmolasses', 'swiss cheese', 'thyme', 'breadfruit', 'pepper', 'hot sauce', 'potato chips',
                            'cornmeal', 'plum tomatoes', 'graham crackers', 'apricot', 'quail', 'almond paste',
                            'almonds', 'melons', 'mozzarella', 'cream', 'focaccia', 'bard', 'pasta', 'cabbage',
                            'rosemary', 'crabs', 'pumpkins', 'oregano', 'bacon', 'milk', 'venison', 'pesto', 'sushi',
                            'lettuce', 'cantaloupes', 'kale', 'eggs', 'shrimp', 'pinto beans', 'tomatoes',
                            'tomato paste', 'celery seeds', 'garlic powder', 'chicken', 'lamb', 'barbecue sauce',
                            'mushrooms', 'salt', 'chicory', 'flour', 'onion', 'coconut oil', 'olives', 'passion fruit',
                            'pea beans', 'cheese', 'tartar sauce', 'pine nuts', 'lobsters', 'plums', 'yogurt',
                            'oranges', 'corn', 'turkeys', 'ale', 'red beans', 'chestnuts', 'truffles', 'cheddar cheese',
                            'basil', 'pickles', 'buttermilk', 'potatoes', 'butter', 'sour cream', 'tarragon',
                            'pork', 'soy beans', 'rice', 'figs', 'salmon', 'hazelnuts', 'broccoli', 'margarine', 'eel',
                            'parsley', 'sauerkraut', 'beef', 'liver', 'mackerel', 'prunes', 'maple syrup', 'apples',
                            'granola', 'pears', 'water', 'ham', 'radishes', 'bagels', 'honey', 'steak', 'macaroni',
                            'pineapples', 'squid', 'cherries', 'walnuts', 'fish sauce', 'cocoa powder',
                            'brussel sprouts', 'garlic', 'ketchup', 'tonic water', 'ginger', 'tuna']

    ''' Unit amounts '''
    ingredient_unit_amt_list = ['1/2', '1/4', '1/5', '3/4', '1/16', '1/8', '3/8', '2/3', '1/6', '1', '2', '3', '4', '5',
                                '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                                '100', '140', '160', '200', '240', '300', '180', '220', '250', '280', '500', '450']

    ''' Ingredient unit '''
    ingredient_unit_list = ['teaspoon', 'tablespoon', 'cup', 'oz', 'quart', 'lb', 'cubic centimeter', 'cm', 'liter',
                            'ml', 'gram', 'kg', 'pint', 'gallon', 'ounce']

    def validation_list(self):
        return ['name', 'result']

    def next_value(self):
        if self.result == 'IngredientType':
            return random.choice(self.ingredient_type_list)
        elif self.result == 'IngredientUnitAmt':
            return random.choice(self.ingredient_unit_amt_list)
        elif self.result == 'IngredientUnit':
            return random.choice(self.ingredient_unit_list)


# ------------------------------------------------------------------------------
class MealType(AbstractDataSet):
    '''
    ds_dict will contain the following:
        {
            "name" : <string value>
        }
    '''

    ''' Valid food types '''
    food_type_list = ['Breakfast', 'Lunch', 'Dinner']

    def validation_list(self):
        return ['name']

    def next_value(self):
        return random.choice(self.food_type_list)


# ------------------------------------------------------------------------------
class DataSetBuilder(object):
    '''
    Returns a new instance of a data set based on
    subclass name (see @get_name function)
    '''

    def __init__(self):
        '''
        __classes will be a dictionary of AbstractDataSet subclasses
        in the following form:
        {
            <__classname__1>:<__class_object__1>,
            <__classname__2>:<__class_object__2>,
            ...
        }
        '''
        # @PydevCodeAnalysisIgnore
        self.classes = {c.__name__: c for c in \
                        AbstractDataSet.__subclasses__()}

    def new(self, name, ds_dict):
        '''
        Returns the instance of the class based on class name .
        Every object instantiated with this method will be instances
        of AbstractDataSet subclasses .
        '''
        return self.classes[name](ds_dict)


# ------------------------------------------------------------------------------
class DataSetEvaluator(object):
    def __init__(self, xml_filename):
        # Build element tree
        self.__elem_tree = ElementTree()
        self.__elem_tree.parse(xml_filename)

        # Initialize class attributes
        self.instances = self.init_instances()
        self.instances_values = self.update_iterations_values()
        self.iterations = int(self.init_iterations())
        self.template = self.init_template()

    def init_instances(self):
        '''
        Parse __elem_tree to determine and new the data
        set objects present in the XML file .
        '''
        # Obtain all the <dataset> elements from the XML file
        instances = {}
        dsb = DataSetBuilder()
        dataset_list = list(self.__elem_tree.iter("dataset"))
        if len(dataset_list) == 0:
            sys.stderr.write('Warning: Data sets not defined.\n')
        for dataset in dataset_list:
            if 'name' in dataset.attrib.keys():
                dataset_name = dataset.attrib['name']
            else:
                sys.stderr.write('Error: Unnamed data set. Aborting .\n')
                sys.stderr.write('Exiting (-1)')
                sys.exit(-1)
            if 'type' in dataset.attrib.keys():
                dataset_type = dataset.attrib['type']
            else:
                sys.stderr.write('Error: Untyped data set. Aborting. \n')
                sys.stderr.write('Exiting (-1)')
                sys.exit(-1)
            # Create the ds_dict for the Abstract Data Set subclasses
            ds_dict = {key: value for (key, value) in dataset.attrib.items() if
                       key != 'type'}
            # Build instances of Data Sets
            if dataset_type not in dsb.classes:
                sys.stderr.write('Error: Unknown type: \'%s\'. Aborting. \n' %
                                 dataset_type)
                sys.stderr.write('Exiting (-1) .\n')
                sys.exit(-1)
            instances[dataset_name] = dsb.new(dataset_type, ds_dict)
        return instances

    def init_iterations(self):
        '''
        Returns the number of iterations (how many subsequent lines
        to generate)
        '''
        return int(self.__elem_tree.getroot().attrib['iterations'])

    def init_template(self):
        '''
        Retrieves the template string from the XML file
        '''
        return self.__elem_tree.findall('template')[0].text

    def update_iterations_values(self):
        '''
        Keep a dictionary with instances values to preserve next_value()
        across iteration .
        '''
        return {key: instance.next_value() for (key, instance) in \
                self.instances.items()}

    def write_output(self, output=sys.stdout):
        '''
        Parse the template and write the output to a stream .
        The default stream is sys.stdout .
        '''
        # Find all #{data_set_names} and replace them with
        # self.instances[data_set_name].next_value()
        regex = '(?:^|(?<=[^#]))#{\w+}'

        def inner_subst(matchobj):
            # Removing unneeded characters from key
            key = matchobj.group(0)
            for c in ['{', '#', '}']:
                key = key.replace(c, '')
            # replace #{word} with instance values .
            return str(self.instances_values[key])

        for i in range(self.iterations):
            if (i % 10000 == 0):
                print i
            output.write(re.sub(regex, inner_subst, self.template))
            self.instances_values = self.update_iterations_values()


# ------------------------------------------------------------------------------

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='  Generate test data.')
    ap.add_argument('-i', '--input', dest='ifile', help='the input file (XML)')
    ap.add_argument('-o', '--output', dest='ofile',
                    help='the output file (TEXT)')

    results = ap.parse_args()
    if results.ifile is None:
        ap.error('Input file (IFILE) cannot be empty')
        sys.exit(-1)

    dsv = DataSetEvaluator(results.ifile)

    if results.ofile is None:
        dsv.write_output()
    else:
        out = open(results.ofile, mode='w')
        dsv.write_output(output=out)
        out.close()
