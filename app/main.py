from client import Parser
from writers import write_data


def main():
    parser = Parser()
    data = parser.get_result_data()
    write_data(data, parser.get_years(), parser.REGION_PREFIX)


if __name__ == '__main__':
    main()
