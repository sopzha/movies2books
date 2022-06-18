import json
from moviepy.editor import *

def timestamp_to_seconds(timestamp):
    [hours, minutes, seconds] = timestamp.split(':')
    return 3600 * float(hours) + 60 * float(minutes) + float(seconds)

def create_alignments_html(book_name):
    with open('./{}/ground_truth_annotation.json'.format(book_name), 'r') as f:
        alignments = json.load(f)
        
    lines = ["<html>",
            "<h2>{}</h2>".format(book_name.replace('_', ' ')),
            "<table>",
            "<tbody>",
            "<tr>",
                "<th>No</th>",
                "<th>Alignment Type</th>",
                "<th>Sentence</th>",
                "<th>Line</th>",
                "<th>Subtitle</th>",
                "<th>Time Shot</th>",
                "<th>Time Clip</th>",
                "<th>Shot</th>",
            "</tr>",
            ]
    
    for i, alignment in enumerate(alignments):
        
        [start_timestamp, end_timestamp] = alignment['Time Shot'].split(' ')
        start = int(timestamp_to_seconds(start_timestamp))
        end = int(timestamp_to_seconds(end_timestamp)) + 1
        shot = VideoFileClip('./{}/movie.m4v'.format(book_name)).subclip(start, end)
        shot.write_videofile('./{}/movie_shots/shot_{}.mp4'.format(book_name, str(i)))
        
        lines.append("<tr>")
        lines.append("<td>{}</td>".format(i))
        lines.extend(["<td>{}</td>".format(alignment['Alignment Type']),
                      "<td>{}</td>".format(alignment['Sentence']),
                      "<td>{}</td>".format(alignment['Line']),
                      "<td>{}</td>".format(alignment['Subtitle']),
                      "<td>{}</td>".format(alignment['Time Shot']),
                      "<td>{}</td>".format(alignment['Time Clip']),
                      "<td><video width='320' height='240' controls>",
                          "<source src={} type='video/mp4'>".format("./" + "/movie_shots/shot_" + str(i) + ".mp4"),
                          "</video>",
                      "</td>"])
        lines.append("</tr>")
        
    lines.extend(['</tbody>', '</table>'])
    lines = [line + "\n" for line in lines]
    
    with open('./{}/alignment_visualization.html'.format(book_name), 'w') as out:
        out.writelines(lines)
        
create_alignments_html('The_Shawshank_Redemption')
