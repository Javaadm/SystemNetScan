#include <stdlib.h>
#include <iostream>
#include <algorithm>
#include <jsoncpp/json/json.h>
#include <fstream>
#include <vector>
#include <string>
#include <stdio.h>
#include <stack>
#include <cmath>


using namespace std;


// A C++ program to find convex hull of a set of points. Refer
// https://www.geeksforgeeks.org/orientation-3-ordered-points/
// for explanation of orientation()
struct Point
{
    int x, y;
};

// A global point needed for  sorting points with reference
// to  the first point Used in compare function of qsort()
Point p0;

// A utility function to find next to top in a stack
Point nextToTop(stack<Point> &S)
{
    Point p = S.top();
    S.pop();
    Point res = S.top();
    S.push(p);
    return res;
}

// A utility function to swap two points
int swap(Point &p1, Point &p2)
{
    Point temp = p1;
    p1 = p2;
    p2 = temp;
}

// A utility function to return square of distance
// between p1 and p2
int distSq(Point p1, Point p2)
{
    return (p1.x - p2.x)*(p1.x - p2.x) +
           (p1.y - p2.y)*(p1.y - p2.y);
}

// To find orientation of ordered triplet (p, q, r).
// The function returns following values
// 0 --> p, q and r are colinear
// 1 --> Clockwise
// 2 --> Counterclockwise
int orientation(Point p, Point q, Point r)
{
    int val = (q.y - p.y) * (r.x - q.x) -
              (q.x - p.x) * (r.y - q.y);

    if (val == 0) return 0;  // colinear
    return (val > 0)? 1: 2; // clock or counterclock wise
}

// A function used by library function qsort() to sort an array of
// points with respect to the first point
int compare(const void *vp1, const void *vp2)
{
    Point *p1 = (Point *)vp1;
    Point *p2 = (Point *)vp2;

    // Find orientation
    int o = orientation(p0, *p1, *p2);
    if (o == 0)
        return (distSq(p0, *p2) >= distSq(p0, *p1))? -1 : 1;

    return (o == 2)? -1: 1;
}

// Prints convex hull of a set of n points.
stack<Point> get_convexHull(vector<Point>& points, int n)
{
    // Find the bottommost point
    int ymin = points[0].y, min = 0;
    for (int i = 1; i < n; i++)
    {
        int y = points[i].y;

        // Pick the bottom-most or chose the left
        // most point in case of tie
        if ((y < ymin) || (ymin == y &&
                           points[i].x < points[min].x))
            ymin = points[i].y, min = i;
    }

    // Place the bottom-most point at first position
    swap(points[0], points[min]);

    // Sort n-1 points with respect to the first point.
    // A point p1 comes before p2 in sorted output if p2
    // has larger polar angle (in counterclockwise
    // direction) than p1
    p0 = points[0];
    cout << "\np0 is:" << p0.x << ", " << p0.y << '\n';
    qsort(&points[1], n-1, sizeof(Point), compare);

    // If two or more points make same angle with p0,
    // Remove all but the one that is farthest from p0
    // Remember that, in above sorting, our criteria was
    // to keep the farthest point at the end when more than
    // one points have same angle.
    int m = 1; // Initialize size of modified array
    for (int i=1; i<n; i++)
    {
        // Keep removing i while angle of i and i+1 is same
        // with respect to p0
        while (i < n-1 && orientation(p0, points[i],
                                      points[i+1]) == 0)
            i++;


        points[m] = points[i];
        m++;  // Update size of modified array
    }

    // If modified array of points has less than 3 points,
    // convex hull is not possible
    if (m < 3) return stack<Point>();

    // Create an empty stack and push first three points
    // to it.
    stack<Point> S;
    S.push(points[0]);
    S.push(points[1]);
    S.push(points[2]);

    // Process remaining n-3 points
    for (int i = 3; i < m; i++)
    {
        // Keep removing top while the angle formed by
        // points next-to-top, top, and points[i] makes
        // a non-left turn
        while (orientation(nextToTop(S), S.top(), points[i]) != 2)
            S.pop();
        S.push(points[i]);
    }

    return S;
    // Now stack has the output points, print contents of stack
    while (!S.empty())
    {
        Point p = S.top();
        cout << "(" << p.x << ", " << p.y <<")" << endl;
        S.pop();
    }
}

bool compare_lines(const pair<Point, Point> & a, const pair<Point, Point> & b)
{
    return distSq(a.first, a.second) > distSq(b.first, b.second);
}

vector<pair<int, int>> get_pass_variety()
{
    string system_path = "/home/mikhail/Work_with_documents/Alpha/C_directory/";
    string open_file = system_path + "image.txt";
    string write_file = system_path + "coordinates_2p.txt";
    ifstream cin;
    cin.open(open_file.c_str());
    int rows, columns;
    cin >> rows >> columns;
    vector<vector<short>> image(rows, vector<short>(columns, 0));
    vector<vector<pair<int, int>>> varieties;
    vector<vector<short>> is_used(rows,vector<short>(columns, false));

    for (int i = 0; i < rows; i++)
        for (int j = 0; j < columns; j++)
            cin >> image[i][j];

    int counter = 0;
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < columns; j++)
            counter += (image[i][j] == 255);
    cout << '\n' << counter << '\n';
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

                //cout << varieties.back().size() << '\n';
            }
        }
    }
    int m = 0;
    sort(varieties.begin(), varieties.end(),
         [](vector<pair<int, int>> & a, vector<pair<int, int>> & b)
         {return a.size() > b.size();});

    for(int i = 0; i < 3; i++)
        cout << '\n' << varieties[i].size();

    int left = columns, right = 0, up = rows, down = 0;
    for (pair<int, int> cur : varieties[0])
    {
        left = min(left, cur.second);
        right = max(right, cur.second);
        up = min(up, cur.first);
        down = max(down, cur.first);
    }

    ofstream cout;
    cout.open(write_file.c_str());
    cout << left << ' ' << up << ' ' << right << ' ' << down;
    return varieties[0];
}



int main() {
    vector<pair<int, int>> pass_variety = get_pass_variety();
    cout << "First of variety" << pass_variety[0].first << ", " << pass_variety[0].second << '\n';
    vector<Point> points;
    for (pair<int, int> point: pass_variety)
    {
       points.push_back(Point());
       points.back().x = point.first;
       points.back().y = point.second;
    }

    stack<Point> convexHull = get_convexHull(points, (int)pass_variety.size());


    fcloseall();
    cout << "\n hull size: " << convexHull.size();

    vector<Point> hull;

    while(convexHull.size())
    {
        hull.push_back(convexHull.top());
        convexHull.pop();
        cout << '\n' << hull.back().x << ", " << hull.back().y;
    }

    vector<pair<Point, Point>> lines;
    for(int i = 0; i < hull.size(); i++)
        for(int j = i+1; j < hull.size(); j++)
        {
            lines.push_back({hull[i], hull[j]});
        }

    sort(lines.begin(), lines.end(), [](const pair<Point, Point> & a, const pair<Point, Point> & b)
            {return distSq(a.first, a.second) > distSq(b.first, b.second);});

    Point line1, line2;
    line1.x = lines[0].first.x - lines[0].second.x;
    line1.y = lines[0].first.y - lines[0].second.y;

    for (int i = 0; i < lines.size(); i++)
    {
        line2.x = lines[i].first.x - lines[i].second.x;
        line2.y = lines[i].first.y - lines[i].second.y;
        float angle1 = atan2(line1.y, line1.x);
        if(angle1 < 0)
            angle1 += M_PI;
        float angle2 = atan2(line2.y, line2.x);
        if(angle2 < 0)
            angle2 += M_PI;

        float dif = abs(angle1 - angle2);
        if(dif > 0.2 && dif < 2.94)
        {
            cout << endl << i << endl;
            lines[1] = lines[i];
            break;
        }
    }

    for (int i = 0; i < 2; i++)
    {
        cout << endl << i << endl;
        cout << lines[i].first.x << ' ' << lines[i].first.y << endl;
        cout << lines[i].second.x << ' ' << lines[i].second.y << endl;
    }

    ofstream diag_out;
    string system_path = "/home/mikhail/Work_with_documents/Alpha/C_directory/";
    diag_out.open((system_path + "coordinates_4p.txt").c_str());
    for (int i = 0; i < 2; i++)
    {
        diag_out << lines[i].first.y << ' ' << lines[i].first.x << ' ';
        diag_out << lines[i].second.y << ' ' << lines[i].second.x;
        if(i == 0)
            diag_out << ' ';
    }
    return 0;
}
