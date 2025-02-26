import unittest
from lizard import  analyze_file, FileAnalyzer, get_extensions
from lizard_languages import JSXReader


def get_jsx_function_list(source_code):
    return analyze_file.analyze_source_code("a.jsx", source_code).function_list

class Test_tokenizing_JSX(unittest.TestCase):

    def check_tokens(self, expect, source):
        tokens = list(JSXReader.generate_tokens(source))
        self.assertEqual(expect, tokens)

    def test_simple_standalone(self):
        self.check_tokens(['<abc />'], '<abc />')

    def test_simple_open_closing(self):
        self.check_tokens(['<abc>', '</abc>'], '<abc></abc>')

    def test_open_closing_with_content(self):
        self.check_tokens(['(', '<abc>', 'xxx', '  ', '+', 'yyy', '</abc>', ')'], '(<abc>xxx  +yyy</abc>)')

    def test_nested(self):
        self.check_tokens(['(', '<abc>', '<b>', 'xxx', '</b>', '</abc>', ')'], '(<abc><b>xxx</b></abc>)')

    def test_nested_save_tag(self):
        self.check_tokens(['(', '<b>', '<b>', 'xxx', '</b>', '</b>', ')'], '(<b><b>xxx</b></b>)')

    def test_with_embeded_code(self):
        self.check_tokens(['<abc>', '{', 'x', '}', '</abc>'], '<abc>{x}</abc>')

    def test_with_attributes(self):
        self.check_tokens(['<abc x="x">a</abc>'], '<abc x="x">a</abc>')

    def test_with_embeded_attributes(self):
        self.check_tokens(['y'], '<abc x={y}>a</abc><a></a>')

    def test_less_than(self):
        self.check_tokens(['a', '<', '3', ' ', 'x', '>'], 'a<3 x>')

    def test_with_less_than2(self):
        self.check_tokens(['a', '<', 'b', ' ', 'and', ' ', 'c', '>', ' ', 'd'], 'a<b and c> d')

    def test_complicated_properties(self):
        self.check_tokens(['data', ' ', '=>', '(', ')'], '<StaticQuery render={data =>()} />')


class Test_parser_for_JavaScript_X(unittest.TestCase):

    def test_simple_function(self):
        functions = get_jsx_function_list("x=>x")
        self.assertEqual("(anonymous)", functions[0].name)

    def test_complicated(self):
        code = '''
          <StaticQuery render={data => ()} />
        '''

        functions = get_jsx_function_list(code)
        self.assertEqual("(anonymous)", functions[0].name)
        
    def test_complex_jsx_attributes(self):
        code = '''
          const GridComponent = () => {
            return (
              <div>
                <Grid
                  getRowId={ (model) => model.id }
                  onClick={ (e) => handleClick(e) }
                  style={{ width: '30%' }}
                  onKeyDown={(e) => { 
                    if (e.key === 'Enter') {
                      doSomething();
                    }
                  }}
                />
              </div>
            );
          }
        '''
        functions = get_jsx_function_list(code)
        # The main function should be parsed correctly
        self.assertEqual("(anonymous)", functions[0].name)
        # The function should have the correct complexity
        self.assertEqual(1, functions[0].cyclomatic_complexity)

