# newspaper
python3 newspaper.py example.pdf

example.pdf -- soningiin zam

Article_lines.py (function) -- ugugdsun zuraasuudaas article ylgah zuraasiig todorhoilno. Mun tedgeeriin ogtloltsoliin zuraasiig hadgalna.

newspaper_order.py (function) -- ugugdsun huudasnii article-uud dotorhi text blockuudiig zuw unshih daraalald oruulna.

newspaper.py -- undsen code

Output/ hawtsas dotor huudas bureer article-g herhen ylgaj buig haruulsan zurag bolon json file garna.

# Ajillaj bui zarchim

1. Newspaper-n pdf file-g unshij awna.

2. Huudas buriig zurag bolgon hurwuulne.

3. line_detection function-r damjuulan huudas deerhi zuraasuudiig ilruulne.

4. PyMuPdf sang ashiglan gargaj awsan pdf deerhi text block-g para_segment function-r damjuulan negtgene.

5. remove_lines function-r damjuulan negtgesen text blocktoi dawhtsaj bui zuraasuudiig hasna.

6. article_lines function-r damjuulan uldsen zuraasaas article huwaaj bui zuraasiig ylgan awna.

7. points_x dotor ogtloltsoj bui tseg, zuraas-n ehlel, tugsguliin tseguudiig hadgalna.

8. tseguudiig ashiglan uusej boloh buh bbox-g uusgene (zuun deed bulangiin tsegees ehluulen haina).

9. uussen bbox-g talbaigaar ni sortlono.

10. jijig talbai bbox-s ehluulen pdf deerhi contentiig bbox ruu oruulan article-uudiig ylgana.

11. ylgasan article-uud dotorhi contentiig reading_order function-r damjuulan zuw daraalald oruulna.

12. article ylgasan bbox-n dugaarlaltiig tsenher unguur, dotorhi content-n dugaarlaltiig har unguur dugaarlasan buguud article buriin bbox-n ungu uur baihaar zuragt durslen gargana.

13. content-g json deer hadgalna. (article_box ni tuhain article-n yerunhii bbox, text dotor dotorh contentiig hadgalsan)
