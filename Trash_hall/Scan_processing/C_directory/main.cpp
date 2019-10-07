#include <iostream>
#include <algorithm>
#include <jsoncpp/json/json.h>
#include <fstream>
#include <vector>
#include <string>
#include <stdio.h>

#pragma comment(linker, "/STACK: 2000000")
using namespace std;

vector<pair<int, int>> get_pass_variety()
{
    string system_path = "/home/mikhail/Work_with_documents/Trash_hall/Scan_processing/C_directory/";
    string open_file = system_path + "image.txt";
    string write_file = system_path + "coordinates_2p.txt";
    freopen(open_file.c_str(),"r", stdin);
    int rows, columns;
    cin >> rows >> columns;
    vector<vector<short>> image(rows, vector<short>(columns, 0));
    vector<vector<pair<int, int>>> varieties;
    vector<vector<short>> is_used(rows,vector<short>(columns, false));

    for (int i = 0; i < rows; i++)
        for (int j = 0; j < columns; j++)
            cin >> image[i][j];

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < columns; j++) {
            if (image[i][j] == 255 && is_used[i][j] == false) {
                //creating a new variety
                varieties.push_back(vector<pair<int, int>>(0));

                vector<pair<int, int>> points;
                points.push_back({i, j});
                while(points.size())
                {
                    int x = points.back().first, y = points.back().second;
                    points.pop_back();
                    //checking x and y
                    if(x < 0 || x >= rows || y < 0 || y >= columns)
                        continue;
                    if(is_used[x][y] || image[x][y] == 0)
                        continue;

                    //adding current value to variety
                    varieties.back().push_back({x, y});
                    is_used[x][y]=true;

                    //trying near points
                    for (int i = -2; i<=2; i++)
                    {
                        for (int j = -2; j<=2; j++)
                        {
                            int new_x = x + i, new_y = y + j;
                            if(new_x < 0 || new_x >= rows || new_y < 0 || new_y >= columns)
                                continue;
                            if(is_used[new_x][new_y] == true,
                                    image[new_x][new_y] == 0)
                                continue;

                            //adding a new point
                            points.push_back({new_x, new_y});
                        }
                    }
                }

                cout << varieties.back().size() << '\n';
            }
        }
    }
    int m = 0;
    sort(varieties.begin(), varieties.end(),
         [](vector<pair<int, int>> & a, vector<pair<int, int>> & b)
         {return a.size() > b.size();});

    for(int i = 0; i < 10; i++)
        cout << '\n' << varieties[i].size();

    int left = columns, right = 0, up = rows, down = 0;
    for (pair<int, int> cur : varieties[0])
    {
        left = min(left, cur.second);
        right = max(right, cur.second);
        up = min(up, cur.first);
        down = max(down, cur.first);
    }

    freopen(write_file.c_str(), "w", stdout);
    cout << left << ' ' << up << ' ' << right << ' ' << down;
    return varieties[0];
}



int main() {
   return 0;
}