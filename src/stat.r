# dependencies
library(svglite)
library(ggplot2)
library(ggpubr)
library(tidyverse)
library(showtext)
font_add_google("M PLUS Rounded 1c", "ja")
showtext_auto()

## External uniformity value

## Visulize external uniformity value (\(U\)) of the selected examples.
## #+NAME: load external uniformity value data

df.ex <- read.csv("../data/ex_valued.csv")
df.ex$lemma <- factor(df.ex$lemma, levels = df.ex$lemma)
df.ex$bg_id <- factor(df.ex$bg_id, levels = df.ex$bg_id)
head(df.ex)



## #+RESULTS[9be2a3530b7d61d984f2223049b5d5997efcc3f5]: load external uniformity value data
## |   |  X | bg_id                                        |      avg_sim | lemma              | rdg                          | num | pos_match | group_match | field_match | annotation | Unnamed..9            | period_a_dist  | period_b_dist  | external_uniformity |
## |---+----+----------------------------------------------+--------------+--------------------+------------------------------+-----+-----------+-------------+-------------+------------+-----------------------+----------------+----------------+---------------------|
## | 1 | 16 | ('BG-01-5510-08-0900', 'BG-01-5510-08-1000') | 0.4645453251 | ('葎', '八重葎')   | ('むぐら', 'やへむぐら')     |   2 | True      | True        | True        |          1 |                       | (0.0, 1.0)     | (0.625, 0.375) |               0.375 |
## | 2 |  6 | ('CH-26-0000-00-0701', 'CH-26-5240-05-0801') | 0.3168492511 | ('大原', '大原山') | ('おほはら', 'おほはらやま') |   2 | True      | False       | False       |          1 |                       | (1.0, 0.0)     | (0.455, 0.545) |   0.454545454545455 |
## | 3 | 14 | ('BG-01-4420-04-1100', 'CH-29-0000-00-1300') | 0.3692124684 | ('神垣', '神奈備') | ('かみがき', 'かむなび')     |   2 | False     | False       | False       |          3 | 神奈備/神垣の三室の山 | (0.1, 0.9)     | (0.5, 0.5)     |                 0.6 |
## | 4 |  8 | ('BG-01-1730-02-0300', 'BG-01-1730-03-0300') | 0.3239619935 | ('此方', '彼方')   | ('こなた', 'あなた')         |   2 | True      | True        | False       |          1 |                       | (0.438, 0.562) | (0.143, 0.857) |   0.705357142857143 |
## | 5 | 18 | ('BG-01-2120-01-0100', 'BG-01-2120-02-2601') | 0.5348400379 | ('親', '垂乳根')   | ('おや', 'たらちね')         |   2 | True      | True        | False       |          1 | 枕詞                  | (0.7, 0.3)     | (0.429, 0.571) |   0.728571428571429 |
## | 6 | 15 | ('BG-01-5620-01-0601', 'BG-01-5620-04-0703') | 0.4587191201 | ('水鳥', '葦鴨')   | ('みづとり', 'あしがも')     |   2 | True      | True        | False       |          1 |                       | (0.5, 0.5)     | (0.75, 0.25)   |                0.75 |

## #+NAME: visualize external uniformity value
## #+headers: :width 15 :height 7

ff <- df.ex %>% 
  ggplot(aes(as.numeric(lemma), external_uniformity)) + 
  geom_bar(stat='identity') +
  ggtitle("") +
  theme_classic() +
  theme(title = element_text(size=20),
        text = element_text(size=20),
        axis.text.x = element_text(angle = -90, vjust = 0.5),
        strip.background = element_rect( colour = "white", fill = "white"), 
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        axis.line = element_blank(),
        axis.line.y = element_line()) +
  ylab("External uniformity value (U)") + xlab("Lexical variable") +
  geom_hline(yintercept = mean(df.ex$external_uniformity),
             linetype = 'dashed',
             color = 'red') +
  scale_x_continuous(breaks = 1:length(df.ex$lemma),
                     labels = df.ex$lemma,
                     sec.axis = sec_axis(~.,
                                         breaks = 1:length(df.ex$lemma),
                                         labels = df.ex$bg_id)) +
  scale_y_continuous(breaks=c(0,0.25,0.5,0.75,1.0)) +
  coord_flip(ylim = c(0, 1.5)) +
  annotate(geom = 'text',
           x = 1:19,
           y = 0.02,
           hjust = 'left',
           color = 'white',
           label = round(df.ex$external_uniformity, 3)) +

  annotate(geom = 'text',
           x = 1:19,
           y = df.ex$external_uniformity + 0.05,
           hjust = 'left',
           label = paste(df.ex$period_a_dist,rep('→',19),df.ex$period_b_dist))

ff %>% ggsave(filename = "../artifact/fig/ex_value.svg", width=15, height=7)
ff
