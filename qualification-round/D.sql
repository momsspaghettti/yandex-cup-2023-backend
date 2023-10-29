WITH RECURSIVE ppr AS (SELECT id, prev_id, id as target, COALESCE(pickup_point_id, 0) as flag
                       FROM pickup_point
                                left join brand_data on id = pickup_point_id
                       WHERE branded_since = :targetDate

                       UNION

                       SELECT pp.id, pp.prev_id, ppr_i.target, COALESCE(bd.pickup_point_id, 0) as flag
                       FROM pickup_point pp
                                INNER JOIN ppr ppr_i ON pp.id = ppr_i.prev_id
                                left join brand_data bd on pp.id = bd.pickup_point_id)
SELECT target
FROM ppr
group by target
having sum(flag) = 0;
